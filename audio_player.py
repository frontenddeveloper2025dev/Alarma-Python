import pygame
import threading
import time
import os
from alarm_sound import AlarmSoundGenerator

class AudioPlayer:
    def __init__(self):
        self.sound_generator = AlarmSoundGenerator()
        self.is_playing = False
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except Exception as e:
            print(f"Error initializing audio: {e}")
    
    def play_alarm_sound(self, duration: int = 30):
        """Play alarm sound for specified duration (seconds)"""
        if self.is_playing:
            return
        
        try:
            # Generate alarm sound
            sound_file = self.sound_generator.generate_alarm_sound()
            
            if sound_file and os.path.exists(sound_file):
                # Start playing in a separate thread
                play_thread = threading.Thread(
                    target=self._play_sound_thread,
                    args=(sound_file, duration),
                    daemon=True
                )
                play_thread.start()
            else:
                print("Could not generate alarm sound")
                
        except Exception as e:
            print(f"Error playing alarm sound: {e}")
    
    def _play_sound_thread(self, sound_file: str, duration: int):
        """Play sound in a separate thread"""
        try:
            self.is_playing = True
            sound = pygame.mixer.Sound(sound_file)
            
            # Play for specified duration
            start_time = time.time()
            while time.time() - start_time < duration:
                sound.play()
                time.sleep(1)  # Play every second
                
                # Check if we should stop
                if not self.is_playing:
                    break
            
            self.is_playing = False
            
            # Clean up temporary file
            try:
                os.remove(sound_file)
            except:
                pass
                
        except Exception as e:
            print(f"Error in sound playing thread: {e}")
            self.is_playing = False
    
    def stop_alarm(self):
        """Stop currently playing alarm"""
        self.is_playing = False
        try:
            pygame.mixer.stop()
        except:
            pass
