import pvporcupine
import pyaudio
import struct


class PorcupineDetector:
    """
    Wake word detector using Porcupine from Picovoice.
    Supports both built-in keywords and custom .ppn files.
    """
    
    def __init__(self, access_key, keywords=None, keyword_paths=None, sensitivity=0.5):
        """
        Initialize Porcupine detector.
        
        Args:
            access_key: Porcupine access key from console.picovoice.ai
            keywords: List of built-in keywords (e.g., ['porcupine', 'alexa'])
            keyword_paths: List of paths to custom .ppn files (optional)
            sensitivity: Detection sensitivity 0.0-1.0 (default 0.5)
        """
        self.access_key = access_key
        self.keywords = keywords or []
        self.keyword_paths = keyword_paths or []
        self.sensitivity = sensitivity
        self.porcupine = None
        self.pa = None
        self.audio_stream = None
        self.is_initialized = False
        
        # Validate that we have at least one keyword
        if not self.keywords and not self.keyword_paths:
            raise ValueError("Must provide either keywords or keyword_paths")
    
    def initialize(self):
        """Initialize Porcupine and audio stream."""
        try:
            # Create Porcupine instance
            if self.keywords:
                # Use built-in keywords
                self.porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keywords=self.keywords,
                    sensitivities=[self.sensitivity] * len(self.keywords)
                )
            else:
                # Use custom keyword paths
                self.porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keyword_paths=self.keyword_paths,
                    sensitivities=[self.sensitivity] * len(self.keyword_paths)
                )
            
            # Initialize PyAudio
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length,
                input_device_index=None
            )
            
            self.is_initialized = True
            print(f"✅ Porcupine initialized successfully!")
            print(f"   Listening for: {self.keywords or self.keyword_paths}")
            print(f"   Sample rate: {self.porcupine.sample_rate} Hz")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Porcupine: {e}")
    
    def detect(self):
        """
        Check if wake word is detected (single frame check).
        
        Returns:
            True if wake word detected, False otherwise
        """
        if not self.is_initialized:
            self.initialize()
        
        try:
            pcm = self.audio_stream.read(
                self.porcupine.frame_length,
                exception_on_overflow=False
            )
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            keyword_index = self.porcupine.process(pcm)
            
            if keyword_index >= 0:
                detected_word = self.keywords[keyword_index] if self.keywords else self.keyword_paths[keyword_index]
                print(f"🎉 Wake word detected: {detected_word}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error during detection: {e}")
            return False
    
    def listen_for_wake_word(self):
        """
        Continuously listen for wake word (blocking).
        Returns when wake word is detected.
        """
        if not self.is_initialized:
            self.initialize()
        
        print("👂 Listening for wake word...")
        
        try:
            while True:
                if self.detect():
                    break
        except KeyboardInterrupt:
            print("\n🛑 Wake word detection stopped by user")
    
    def cleanup(self):
        """Clean up resources."""
        if self.audio_stream is not None:
            self.audio_stream.close()
        if self.pa is not None:
            self.pa.terminate()
        if self.porcupine is not None:
            self.porcupine.delete()
        self.is_initialized = False
    
    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
        return False