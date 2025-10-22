class Speaker:
    def __init__(self, tts_engine):
        self.tts_engine = tts_engine

    def speak(self, text):
        self.tts_engine.synthesize(text)
        self.tts_engine.play()