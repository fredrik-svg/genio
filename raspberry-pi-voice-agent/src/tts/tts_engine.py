import subprocess
import wave
import io
import sounddevice as sd
import numpy as np
from pathlib import Path


class PiperTTS:
    """Piper TTS engine for high-quality local text-to-speech synthesis."""
    
    def __init__(self, model_path, config_path=None, language='sv'):
        """
        Initialize Piper TTS engine.
        
        Args:
            model_path: Path to the Piper ONNX model file
            config_path: Path to the model config JSON file (optional)
            language: Language code (default: 'sv' for Swedish)
        """
        self.model_path = Path(model_path)
        self.config_path = Path(config_path) if config_path else None
        self.language = language
        self.sample_rate = 22050  # Default Piper sample rate
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"Piper model not found at {self.model_path}")
    
    def synthesize(self, text):
        """
        Synthesize text to speech using Piper.
        
        Args:
            text: Text to synthesize
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            # Build Piper command
            cmd = ['piper', '--model', str(self.model_path), '--output-raw']
            
            if self.config_path and self.config_path.exists():
                cmd.extend(['--config', str(self.config_path)])
            
            # Run Piper and capture output
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Send text and get audio output
            audio_data, error = process.communicate(input=text.encode('utf-8'))
            
            if process.returncode != 0:
                raise RuntimeError(f"Piper TTS error: {error.decode('utf-8')}")
            
            # Convert raw audio to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            return audio_array, self.sample_rate
            
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")
    
    def speak(self, text):
        """
        Synthesize and play text to speech.
        
        Args:
            text: Text to speak
        """
        audio_data, sample_rate = self.synthesize(text)
        
        # Play audio using sounddevice
        sd.play(audio_data, sample_rate)
        sd.wait()  # Wait until audio is finished playing
    
    def save_to_file(self, text, filename):
        """
        Synthesize text and save to WAV file.
        
        Args:
            text: Text to synthesize
            filename: Output WAV file path
        """
        audio_data, sample_rate = self.synthesize(text)
        
        # Save as WAV file
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
    
    def set_language(self, language):
        """
        Set the language (note: requires loading a new model).
        
        Args:
            language: Language code
        """
        self.language = language


# Alias for backward compatibility
TTS = PiperTTS