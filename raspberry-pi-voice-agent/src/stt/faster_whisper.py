from faster_whisper import WhisperModel

class FasterWhisperSTT:
    def __init__(self, model_size="base", language="sv"):
        self.model = WhisperModel(model_size, device="cuda" if self._is_cuda_available() else "cpu", language=language)

    def _is_cuda_available(self):
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def transcribe(self, audio_file):
        segments, _ = self.model.transcribe(audio_file, beam_size=5)
        return " ".join(segment.text for segment in segments)

    def transcribe_from_stream(self, audio_stream):
        segments, _ = self.model.transcribe(audio_stream, beam_size=5)
        return " ".join(segment.text for segment in segments)

# Alias för backward compatibility
FasterWhisper = FasterWhisperSTT