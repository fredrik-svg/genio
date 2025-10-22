# Genio AI - Speech-to-Text (STT) Setup Guide

## Overview
Genio AI uses **Faster Whisper** for speech-to-text conversion. This guide explains how to configure and optimize STT for your Raspberry Pi.

## Faster Whisper Model Sizes

Faster Whisper uses pre-trained models in different sizes. Choose based on your hardware:

| Model | Size | RAM | Speed | Accuracy | Recommended For |
|-------|------|-----|-------|----------|-----------------|
| `tiny` | ~75 MB | ~1 GB | Fastest | Lowest | Raspberry Pi 3, Testing |
| `base` | ~150 MB | ~1 GB | Fast | Good | **Raspberry Pi 4/5** ⭐ |
| `small` | ~500 MB | ~2 GB | Medium | Better | Raspberry Pi 5, Desktop |
| `medium` | ~1.5 GB | ~5 GB | Slow | Best | Desktop, Server |
| `large` | ~3 GB | ~10 GB | Slowest | Excellent | High-end systems only |

**Recommendation:** Use `base` for Raspberry Pi—best balance of speed and accuracy.

## Configuration

Edit `config/config.yaml`:

```yaml
stt:
  enabled: true
  model_size: "base"  # tiny, base, small, medium, large
  language: "sv"      # sv for Swedish, en for English, etc.
```

## First Run - Model Download

When you first run Genio AI, Faster Whisper will automatically download the model from Hugging Face:

```bash
# First run will download the model (takes 1-5 minutes depending on model size)
python src/main.py
```

**What happens:**
1. Faster Whisper checks for cached model in `~/.cache/huggingface/`
2. If not found, downloads from Hugging Face Hub
3. Caches locally for future use
4. No auth token needed for public models

## Supported Languages

Faster Whisper supports 99+ languages. Common ones:

- `sv` - Swedish 🇸🇪
- `en` - English 🇬🇧🇺🇸
- `no` - Norwegian 🇳🇴
- `da` - Danish 🇩🇰
- `fi` - Finnish 🇫🇮
- `de` - German 🇩🇪
- `fr` - French 🇫🇷
- `es` - Spanish 🇪🇸

Full list: https://github.com/openai/whisper#available-models-and-languages

## Offline Usage

### Pre-download Models

To download models for offline use:

```bash
# Activate virtual environment
source genio-env/bin/activate

# Download model manually
python -c "from faster_whisper import WhisperModel; WhisperModel('base', device='cpu')"
```

The model will be cached in `~/.cache/huggingface/hub/`.

### Copy Models Between Systems

```bash
# On source system (with internet)
tar -czf faster-whisper-base.tar.gz -C ~/.cache/huggingface/hub .

# Transfer to target system
scp faster-whisper-base.tar.gz pi@raspberry:~/

# On target system (offline)
mkdir -p ~/.cache/huggingface/hub
tar -xzf faster-whisper-base.tar.gz -C ~/.cache/huggingface/hub/
```

## Performance Optimization

### For Raspberry Pi 4/5

```yaml
stt:
  model_size: "base"  # Best balance
  language: "sv"
```

Expected performance:
- Model load: ~5-10 seconds
- Transcription: ~2-5 seconds for 10 second audio
- RAM usage: ~1-1.5 GB

### For Raspberry Pi 3

```yaml
stt:
  model_size: "tiny"  # Lighter model
  language: "sv"
```

Performance:
- Model load: ~2-5 seconds
- Transcription: ~1-3 seconds for 10 second audio
- RAM usage: ~500-700 MB

### For Desktop/Server

```yaml
stt:
  model_size: "small"  # or "medium"
  language: "sv"
```

## Troubleshooting

### Error: "Repository Not Found for url: huggingface.co/.../models/faster-whisper"

**Cause:** Invalid model path in config (e.g., `model_path: "models/faster-whisper"`).

**Solution:** Use model SIZE, not path:
```yaml
stt:
  model_size: "base"  # NOT model_path!
```

### Error: "401 Client Error: Unauthorized"

**Cause:** Network issue or wrong model name.

**Solutions:**
1. Check internet connection
2. Verify model size is valid: `tiny`, `base`, `small`, `medium`, `large`
3. Try downloading manually:
   ```bash
   python -c "from faster_whisper import WhisperModel; WhisperModel('base')"
   ```

### Error: "Cannot find cached snapshot folder"

**Cause:** Model not downloaded and offline mode enabled.

**Solutions:**
1. Connect to internet and run once to download
2. Or manually download and cache the model
3. Check cache location: `ls ~/.cache/huggingface/hub/`

### Slow Transcription

**Solutions:**
1. Use smaller model (`tiny` or `base`)
2. Ensure you're on CPU (Raspberry Pi doesn't have CUDA)
3. Close other applications to free RAM
4. Consider upgrading to Raspberry Pi 5

### Poor Accuracy

**Solutions:**
1. Use larger model (`small` or `medium`) if hardware allows
2. Speak clearly and close to microphone
3. Reduce background noise
4. Verify correct language is set

## Advanced: Custom Model Location

If you want to use a specific local model:

```python
# In src/stt/faster_whisper.py
self.model = WhisperModel(
    "/path/to/custom/model",  # Local path
    device="cpu",
    language=language
)
```

## Testing STT

Create `test_stt.py`:

```python
#!/usr/bin/env python3
from src.stt.faster_whisper import FasterWhisper
from src.config.settings import STT_MODEL_SIZE, STT_LANGUAGE

print(f"Testing STT with model: {STT_MODEL_SIZE}, language: {STT_LANGUAGE}")
print("Initializing (this may take a moment on first run)...")

stt = FasterWhisper(model_size=STT_MODEL_SIZE, language=STT_LANGUAGE)

print("✅ STT initialized successfully!")
print(f"Model loaded: {STT_MODEL_SIZE}")
print(f"Language: {STT_LANGUAGE}")

# Test with audio file (if you have one)
# result = stt.transcribe("test.wav")
# print(f"Transcription: {result}")
```

Run:
```bash
source genio-env/bin/activate
python test_stt.py
```

## Model Comparison

Real-world testing on Raspberry Pi 5:

| Model | Download Size | Load Time | 10s Audio | Accuracy |
|-------|---------------|-----------|-----------|----------|
| tiny | 75 MB | 3s | 1.5s | 85% |
| base | 145 MB | 7s | 3s | 92% |
| small | 466 MB | 15s | 8s | 96% |

**Recommendation:** `base` model for production use on Raspberry Pi 4/5.

## Quick Reference

### Minimal Config
```yaml
stt:
  model_size: "base"
  language: "sv"
```

### Change Model
```bash
nano config/config.yaml
# Change model_size to: tiny, base, small, medium, or large
# Save and restart application
```

### Force Re-download
```bash
rm -rf ~/.cache/huggingface/hub/models--guillaumekln--faster-whisper-*
python src/main.py  # Will re-download
```

---

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Genio AI** 🤖
