import pyaudio
import wave

class Microphone:
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=self.rate,
                                       input=True,
                                       frames_per_buffer=self.chunk)

    def listen(self):
        frames = []
        try:
            while True:
                data = self.stream.read(self.chunk)
                frames.append(data)
        except KeyboardInterrupt:
            print("Recording stopped.")
            self.stop()
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