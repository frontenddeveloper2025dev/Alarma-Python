import numpy as np
import wave
import tempfile
import os

class AlarmSoundGenerator:
    def __init__(self):
        self.sample_rate = 22050
        self.duration = 2.0  # Duration of each alarm beep
    
    def generate_alarm_sound(self) -> str:
        """Generate a simple alarm sound and return the file path"""
        try:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.close()
            
            # Generate alarm sound - classic beeping pattern
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
            
            # Create a beeping pattern: 800Hz for 0.5s, silence for 0.5s, repeat
            frequency1 = 800  # Primary frequency
            frequency2 = 1000  # Secondary frequency for variation
            
            # Generate the waveform
            wave1 = np.sin(2 * np.pi * frequency1 * t)
            wave2 = np.sin(2 * np.pi * frequency2 * t)
            
            # Create beeping pattern
            beep_pattern = np.zeros_like(t)
            
            # First beep (0.0 - 0.3s)
            mask1 = (t >= 0.0) & (t < 0.3)
            beep_pattern[mask1] = wave1[mask1]
            
            # Second beep (0.5 - 0.8s)
            mask2 = (t >= 0.5) & (t < 0.8)
            beep_pattern[mask2] = wave2[mask2]
            
            # Third beep (1.0 - 1.3s)
            mask3 = (t >= 1.0) & (t < 1.3)
            beep_pattern[mask3] = wave1[mask3]
            
            # Apply envelope to avoid clicks
            envelope = np.ones_like(beep_pattern)
            fade_samples = int(0.01 * self.sample_rate)  # 10ms fade
            
            for i in range(len(envelope)):
                if i < fade_samples:
                    envelope[i] = i / fade_samples
                elif i > len(envelope) - fade_samples:
                    envelope[i] = (len(envelope) - i) / fade_samples
            
            beep_pattern *= envelope
            
            # Normalize and convert to 16-bit
            beep_pattern = np.clip(beep_pattern * 0.3, -1.0, 1.0)  # Reduce volume
            audio_data = (beep_pattern * 32767).astype(np.int16)
            
            # Write to WAV file
            with wave.open(temp_file.name, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            
            return temp_file.name
            
        except Exception as e:
            print(f"Error generating alarm sound: {e}")
            return None
    
    def generate_simple_tone(self, frequency: int = 800) -> str:
        """Generate a simple tone as fallback"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.close()
            
            t = np.linspace(0, 1.0, int(self.sample_rate * 1.0))
            wave_data = np.sin(2 * np.pi * frequency * t) * 0.3
            audio_data = (wave_data * 32767).astype(np.int16)
            
            with wave.open(temp_file.name, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            
            return temp_file.name
            
        except Exception as e:
            print(f"Error generating simple tone: {e}")
            return None
