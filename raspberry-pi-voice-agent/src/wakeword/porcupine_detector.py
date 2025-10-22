import pvporcupine
import pyaudio
import struct
import time

class PorcupineDetector:
    def __init__(self, access_key, keyword_paths, sensitivity=0.5):
        self.access_key = access_key
        self.keyword_paths = keyword_paths
        self.sensitivity = sensitivity
        self.porcupine = None
        self.pa = None
        self.audio_stream = None

    def initialize(self):
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=self.keyword_paths,
            sensitivities=[self.sensitivity] * len(self.keyword_paths)
        )
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def listen_for_wake_word(self):
        print("Listening for wake word...")
        while True:
            pcm = self.audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                print(f"Detected wake word: {self.keyword_paths[keyword_index]}")
                break

    def cleanup(self):
        if self.audio_stream is not None:
            self.audio_stream.close()
        if self.pa is not None:
            self.pa.terminate()
        if self.porcupine is not None:
            self.porcupine.delete()