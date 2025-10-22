# Fix: Faster Whisper Language Parameter Error

**Date:** 2025-10-22  
**Issue:** TypeError when initializing WhisperModel with language parameter

## The Problem

When running Genio AI, you might encounter this error:

```
TypeError: __init__(): incompatible constructor arguments. The following argument types are supported:
    1. ctranslate2._ext.Whisper(model_path: str, device: str = 'cpu', ...)

Invoked with: ...; kwargs: device='cpu', ..., language='sv'
```

## Root Cause

The `WhisperModel` class from `faster-whisper` **does not accept** `language` as a constructor parameter. The language should be specified when calling the `transcribe()` method, not during model initialization.

### Incorrect Code (Before Fix):
```python
# ❌ This causes the error
self.model = WhisperModel(model_size, device="cpu", language=language)
```

### Correct Code (After Fix):
```python
# ✅ Store language as instance variable
self.language = language
self.model = WhisperModel(model_size, device="cpu")

# ✅ Use language during transcription
segments, _ = self.model.transcribe(audio_file, language=self.language)
```

## Files Modified

### 1. `src/stt/faster_whisper.py`

**Changed:**
- Removed `language` parameter from `WhisperModel()` initialization
- Stored language as `self.language`
- Added `language=self.language` to both `transcribe()` methods

**Before:**
```python
def __init__(self, model_size="base", language="sv"):
    self.model = WhisperModel(model_size, device="cuda" if self._is_cuda_available() else "cpu", language=language)

def transcribe(self, audio_file):
    segments, _ = self.model.transcribe(audio_file, beam_size=5)
    return " ".join(segment.text for segment in segments)
```

**After:**
```python
def __init__(self, model_size="base", language="sv"):
    self.language = language
    self.model = WhisperModel(model_size, device="cuda" if self._is_cuda_available() else "cpu")

def transcribe(self, audio_file):
    segments, _ = self.model.transcribe(audio_file, beam_size=5, language=self.language)
    return " ".join(segment.text for segment in segments)
```

### 2. `STT_SETUP.md`

Updated the "Advanced: Custom Model Location" section to show correct usage.

### 3. `TROUBLESHOOTING.md`

Added this error as Problem #1 with explanation and solution.

## Why This Happened

The `faster-whisper` library wraps CTranslate2's Whisper implementation, which:
- Accepts model configuration parameters during initialization
- Accepts transcription parameters (including language) during the transcribe call
- Does **not** accept `language` during model initialization

This is different from the original OpenAI Whisper API, which can be confusing.

## Verification

After applying the fix, test with:

```bash
source genio-env/bin/activate
python src/main.py
```

You should see the model load successfully without the TypeError.

## Additional Resources

- **Faster Whisper Documentation:** https://github.com/guillaumekln/faster-whisper
- **CTranslate2 Whisper API:** https://opennmt.net/CTranslate2/python/ctranslate2.models.Whisper.html
- **STT Setup Guide:** [STT_SETUP.md](STT_SETUP.md)

---

**Status:** ✅ Fixed in commit from 2025-10-22

**Genio AI** 🤖
