# Genio AI - All Applied Fixes (2025-10-22)

This document summarizes all fixes applied to resolve STT (Speech-to-Text) configuration issues.

## Fix #1: Faster Whisper Language Parameter Error ✅

### Issue
```
TypeError: __init__(): incompatible constructor arguments
...
Invoked with: ...; kwargs: device='cpu', ..., language='sv'
```

### Root Cause
The `WhisperModel` constructor from `faster-whisper` library does **not accept** `language` as an initialization parameter. The language must be specified during transcription, not during model initialization.

### Files Modified

#### 1. `src/stt/faster_whisper.py` ✅
**Changed:**
- Removed `language` parameter from `WhisperModel()` initialization
- Stored language as instance variable: `self.language = language`
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

#### 2. `STT_SETUP.md` ✅
Updated the "Advanced: Custom Model Location" section with correct usage pattern and a note explaining that `language` should be passed to `transcribe()`, not `WhisperModel()`.

#### 3. `TROUBLESHOOTING.md` ✅
Added this error as **Problem #1** with full explanation and solution code.

#### 4. `FIX_LANGUAGE_PARAMETER.md` ✅
Created detailed documentation explaining the fix.

---

## Fix #2: STT Model Configuration Error ✅

### Issue
```
RepositoryNotFoundError: 401 Client Error
Repository Not Found for url: https://huggingface.co/api/models/models/faster-whisper/
```

### Root Cause
`config.yaml` had an invalid model path configuration. Faster-whisper was treating `"path/to/faster_whisper/model"` as a Hugging Face repository ID.

### Solution
Changed from using `model_path` to `model_size` with valid size names.

### Files Modified

#### 1. `config/config.yaml` ✅
**Changed:**
```yaml
# Before (incorrect):
stt:
  model_path: "path/to/faster_whisper/model"

# After (correct):
stt:
  model_size: "base"  # tiny, base, small, medium, large
  language: "sv"
```

#### 2. `src/config/settings.py` ✅
**Changed:**
- `STT_MODEL_PATH` → `STT_MODEL_SIZE` (with default: "base")
- Added backward compatibility support

#### 3. `src/main.py` ✅
**Changed:**
- Updated imports to use `STT_MODEL_SIZE`
- Changed `FasterWhisper` initialization to use `model_size` parameter

#### 4. `.env.example` ✅
**Changed:**
- `STT_MODEL_PATH` → `STT_MODEL_SIZE`
- Added helpful comments about model sizes

#### 5. `STT_SETUP.md` ✅
Created comprehensive guide with:
- Model size comparison table
- Performance benchmarks for Raspberry Pi
- Supported languages list
- Troubleshooting section

#### 6. `TROUBLESHOOTING.md` ✅
Added as **Problem #2** with model size options.

#### 7. `FIX_STT_MODEL.md` ✅
Created detailed fix documentation.

---

## Available Model Sizes

| Model | Size | RAM | Speed | Accuracy | Best For |
|-------|------|-----|-------|----------|----------|
| `tiny` | ~75 MB | ~1 GB | Fastest | Lowest | Testing, Pi 3 |
| `base` | ~150 MB | ~1 GB | Fast | Good | **Raspberry Pi 4/5** ⭐ |
| `small` | ~500 MB | ~2 GB | Medium | Better | Pi 5, Desktop |
| `medium` | ~1.5 GB | ~5 GB | Slow | Best | Desktop |
| `large` | ~3 GB | ~10 GB | Slowest | Excellent | High-end only |

**Recommendation:** Use `base` for Raspberry Pi.

---

## Configuration Reference

### Minimal Working Configuration

**config/config.yaml:**
```yaml
wakeword_detection:
  access_key: "YOUR_KEY_HERE"  # Get from https://console.picovoice.ai/
  keyword: "porcupine"
  sensitivity: 0.5

stt:
  model_size: "base"
  language: "sv"

tts:
  engine: "piper"
  language: "sv"
  model_path: "models/sv_SE-nst-medium.onnx"
  config_path: "models/sv_SE-nst-medium.onnx.json"

mqtt:
  broker: "mqtt://your-broker.com"
  port: 8883
  username: "user"
  password: "pass"
```

### Alternative: .env Configuration

```bash
PORCUPINE_ACCESS_KEY=your_key_here
WAKE_WORD=porcupine
STT_MODEL_SIZE=base
STT_LANGUAGE=sv
MQTT_BROKER=mqtt://your-broker.com
MQTT_PORT=8883
MQTT_USERNAME=user
MQTT_PASSWORD=pass
```

---

## Testing After Fixes

### 1. Test STT Initialization
```bash
source genio-env/bin/activate
python -c "from src.stt.faster_whisper import FasterWhisper; stt = FasterWhisper(model_size='base', language='sv'); print('✅ STT initialized successfully!')"
```

### 2. Run Full Application
```bash
source genio-env/bin/activate
python src/main.py
```

Expected behavior:
- ✅ First run downloads the "base" model (~150MB, takes 2-5 minutes)
- ✅ Model is cached in `~/.cache/huggingface/`
- ✅ Subsequent runs are instant
- ✅ No TypeError or RepositoryNotFoundError

---

## Documentation Files Created/Updated

1. ✅ **FIX_LANGUAGE_PARAMETER.md** - Detailed fix for language parameter error
2. ✅ **FIX_STT_MODEL.md** - Detailed fix for model configuration error
3. ✅ **STT_SETUP.md** - Comprehensive STT setup guide
4. ✅ **TROUBLESHOOTING.md** - Updated with both STT errors
5. ✅ **README.md** - Added link to STT_SETUP.md
6. ✅ **FIXES_APPLIED.md** - This file

---

## Why These Fixes Were Needed

### faster-whisper Library Architecture

The `faster-whisper` library wraps CTranslate2's Whisper implementation:

```
faster-whisper → ctranslate2 → Whisper Model
```

**Design decisions:**
- Model configuration (device, compute_type) happens at initialization
- Transcription parameters (language, beam_size) happen at transcription time
- This differs from OpenAI's original Whisper API

**Model loading:**
- Accepts model **size names** (tiny/base/small/medium/large)
- Accepts local **directory paths** containing converted models
- Does NOT accept file paths or arbitrary repository IDs
- Automatically downloads from Hugging Face Hub when given size names

---

## Common Mistakes to Avoid

❌ **Don't do this:**
```python
# Wrong: language in WhisperModel initialization
model = WhisperModel(model_size, device="cpu", language="sv")

# Wrong: using file path instead of model size
stt:
  model_path: "path/to/model.bin"

# Wrong: using repository ID format
stt:
  model_path: "models/faster-whisper"
```

✅ **Do this:**
```python
# Correct: language in transcribe() method
self.language = language
model = WhisperModel(model_size, device="cpu")
segments, _ = model.transcribe(audio, language=self.language)

# Correct: use model size names
stt:
  model_size: "base"

# Correct: use valid size or local directory
stt:
  model_size: "base"  # OR
  model_size: "/path/to/converted/model/directory"
```

---

## Status: All Fixed ✅

Both major STT configuration issues have been resolved:
1. ✅ Language parameter error fixed
2. ✅ Model configuration error fixed

**Genio AI is now ready to run!**

Next steps:
1. Configure your Porcupine access key
2. Configure MQTT broker settings
3. Run `python src/main.py`

---

**Date Fixed:** 2025-10-22  
**Genio AI** 🤖
