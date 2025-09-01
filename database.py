import sqlite3
import datetime
import json
from typing import List, Dict, Optional

class AlarmDatabase:
    def __init__(self, db_path: str = "alarms.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create alarms table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alarms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    time TEXT NOT NULL,
                    days TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create alarm_history table for tracking triggered alarms
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alarm_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alarm_id INTEGER,
                    alarm_name TEXT,
                    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (alarm_id) REFERENCES alarms (id)
                )
            ''')
            
            conn.commit()
    
    def create_alarm(self, name: str, time: datetime.time, days: List[str]) -> bool:
        """Create a new alarm"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alarms (name, time, days)
                    VALUES (?, ?, ?)
                ''', (name, time.strftime("%H:%M"), json.dumps(days)))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error creating alarm: {e}")
            return False
    
    def get_all_alarms(self) -> List[Dict]:
        """Get all alarms"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, time, days, is_active, created_at
                    FROM alarms
                    ORDER BY time
                ''')
                
                alarms = []
                for row in cursor.fetchall():
                    alarms.append({
                        'id': row[0],
                        'name': row[1],
                        'time': row[2],
                        'days': json.loads(row[3]),
                        'is_active': bool(row[4]),
                        'created_at': row[5]
                    })
                return alarms
        except Exception as e:
            print(f"Error getting alarms: {e}")
            return []
    
    def get_active_alarms(self) -> List[Dict]:
        """Get only active alarms"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, time, days, is_active, created_at
                    FROM alarms
                    WHERE is_active = 1
                    ORDER BY time
                ''')
                
                alarms = []
                for row in cursor.fetchall():
                    alarms.append({
                        'id': row[0],
                        'name': row[1],
                        'time': row[2],
                        'days': json.loads(row[3]),
                        'is_active': bool(row[4]),
                        'created_at': row[5]
                    })
                return alarms
        except Exception as e:
            print(f"Error getting active alarms: {e}")
            return []
    
    def toggle_alarm(self, alarm_id: int) -> bool:
        """Toggle alarm active status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE alarms 
                    SET is_active = NOT is_active 
                    WHERE id = ?
                ''', (alarm_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error toggling alarm: {e}")
            return False
    
    def delete_alarm(self, alarm_id: int) -> bool:
        """Delete an alarm"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM alarms WHERE id = ?', (alarm_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting alarm: {e}")
            return False
    
    def log_alarm_trigger(self, alarm_id: int, alarm_name: str):
        """Log when an alarm is triggered"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alarm_history (alarm_id, alarm_name)
                    VALUES (?, ?)
                ''', (alarm_id, alarm_name))
                conn.commit()
        except Exception as e:
            print(f"Error logging alarm trigger: {e}")
    
    def get_recent_triggered_alarms(self, limit: int = 5) -> List[Dict]:
        """Get recently triggered alarms"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT alarm_id, alarm_name, triggered_at
                    FROM alarm_history
                    ORDER BY triggered_at DESC
                    LIMIT ?
                ''', (limit,))
                
                history = []
                for row in cursor.fetchall():
                    history.append({
                        'alarm_id': row[0],
                        'name': row[1],
                        'triggered_at': row[2]
                    })
                return history
        except Exception as e:
            print(f"Error getting alarm history: {e}")
            return []
    
    def get_next_alarm(self) -> Optional[Dict]:
        """Get the next alarm that will trigger"""
        active_alarms = self.get_active_alarms()
        if not active_alarms:
            return None
        
        now = datetime.datetime.now()
        current_weekday = now.strftime('%A').lower()
        
        # Map weekday names to numbers
        weekday_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        next_alarm = None
        next_trigger_time = None
        
        for alarm in active_alarms:
            alarm_time = datetime.datetime.strptime(alarm['time'], "%H:%M").time()
            
            for day in alarm['days']:
                # Calculate next occurrence of this alarm
                days_ahead = weekday_map[day] - now.weekday()
                
                if days_ahead < 0:  # Target day already happened this week
                    days_ahead += 7
                elif days_ahead == 0:  # Target day is today
                    if alarm_time > now.time():
                        # Alarm is later today
                        days_ahead = 0
                    else:
                        # Alarm already passed today, next week
                        days_ahead = 7
                
                trigger_time = now + datetime.timedelta(days=days_ahead)
                trigger_time = trigger_time.replace(
                    hour=alarm_time.hour,
                    minute=alarm_time.minute,
                    second=0,
                    microsecond=0
                )
                
                if next_trigger_time is None or trigger_time < next_trigger_time:
                    next_trigger_time = trigger_time
                    next_alarm = alarm.copy()
                    next_alarm['next_trigger'] = trigger_time
        
        return next_alarm
