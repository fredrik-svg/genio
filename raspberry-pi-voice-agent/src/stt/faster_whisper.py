from faster_whisper import WhisperModel
import numpy as np

class FasterWhisperSTT:
    def __init__(self, model_size="base", language="sv"):
        self.language = language
        self.model = WhisperModel(model_size, device="cuda" if self._is_cuda_available() else "cpu")

    def _is_cuda_available(self):
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def transcribe(self, audio_file):
        # Convert raw audio bytes to numpy array if needed
        audio_input = audio_file
        if isinstance(audio_file, bytes):
            # Convert 16-bit PCM audio bytes to float32 numpy array
            audio_int16 = np.frombuffer(audio_file, dtype=np.int16)
            audio_input = audio_int16.astype(np.float32) / 32768.0
        
        segments, _ = self.model.transcribe(audio_input, beam_size=5, language=self.language)
        return " ".join(segment.text for segment in segments)

    def transcribe_from_stream(self, audio_stream):
        # Convert raw audio bytes to numpy array if needed
        audio_input = audio_stream
        if isinstance(audio_stream, bytes):
            # Convert 16-bit PCM audio bytes to float32 numpy array
            audio_int16 = np.frombuffer(audio_stream, dtype=np.int16)
            audio_input = audio_int16.astype(np.float32) / 32768.0
        
        segments, _ = self.model.transcribe(audio_input, beam_size=5, language=self.language)
        return " ".join(segment.text for segment in segments)

# Alias för backward compatibility
FasterWhisper = FasterWhisperSTT