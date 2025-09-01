import threading
import time
import datetime
from typing import Dict
from database import AlarmDatabase
from audio_player import AudioPlayer

class AlarmMonitor:
    def __init__(self, db: AlarmDatabase):
        self.db = db
        self.audio_player = AudioPlayer()
        self.is_running = False
        self.triggered_today = set()  # Track alarms triggered today to avoid duplicates
        
    def start_monitoring(self):
        """Start monitoring alarms in background"""
        self.is_running = True
        
        while self.is_running:
            try:
                self.check_alarms()
                # Check every 30 seconds
                time.sleep(30)
            except Exception as e:
                print(f"Error in alarm monitoring: {e}")
                time.sleep(60)  # Wait longer if there's an error
    
    def stop_monitoring(self):
        """Stop monitoring alarms"""
        self.is_running = False
    
    def check_alarms(self):
        """Check if any alarms should trigger now"""
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_weekday = now.strftime('%A').lower()
        today_key = now.strftime("%Y-%m-%d")
        
        # Reset triggered alarms at midnight
        if now.hour == 0 and now.minute == 0:
            self.triggered_today.clear()
        
        active_alarms = self.db.get_active_alarms()
        
        for alarm in active_alarms:
            # Check if this alarm should trigger now
            if (alarm['time'] == current_time and 
                current_weekday in alarm['days']):
                
                # Create unique key for this alarm today
                alarm_key = f"{alarm['id']}_{today_key}"
                
                # Only trigger if not already triggered today
                if alarm_key not in self.triggered_today:
                    self.trigger_alarm(alarm)
                    self.triggered_today.add(alarm_key)
    
    def trigger_alarm(self, alarm: Dict):
        """Trigger an alarm - play sound and log"""
        try:
            print(f"🔔 Triggering alarm: {alarm['name']} at {alarm['time']}")
            
            # Log the alarm trigger
            self.db.log_alarm_trigger(alarm['id'], alarm['name'])
            
            # Play alarm sound
            self.audio_player.play_alarm_sound()
            
        except Exception as e:
            print(f"Error triggering alarm {alarm['name']}: {e}")
