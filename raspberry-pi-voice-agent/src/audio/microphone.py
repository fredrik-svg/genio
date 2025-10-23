import pyaudio
import wave

class Microphone:
    def __init__(self, rate=16000, chunk=1024, record_seconds=5):
        self.rate = rate
        self.chunk = chunk
        self.record_seconds = record_seconds
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=self.rate,
                                       input=True,
                                       frames_per_buffer=self.chunk)

    def listen(self, duration=None):
        """
        Record audio for a specified duration.
        
        Args:
            duration: Recording duration in seconds. If None, uses self.record_seconds.
        
        Returns:
            bytes: Recorded audio data
        """
        if duration is None:
            duration = self.record_seconds
            
        frames = []
        num_chunks = int(self.rate / self.chunk * duration)
        
        try:
            print(f"🎤 Recording for {duration} seconds...")
            for i in range(num_chunks):
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                frames.append(data)
            print("✅ Recording complete!")
        except KeyboardInterrupt:
            print("⚠️  Recording stopped by user.")
        
        return b''.join(frames)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save(self, filename):
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(self.listen())