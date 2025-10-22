# Genio AI - Quick Start Guide

## ✅ STT Language Fix Applied Successfully!

The warning you saw:
```
[ctranslate2] [warning] The compute type inferred from the saved model is float16...
```

This is **normal and expected** on Raspberry Pi! The model automatically converts from float16 to float32 for CPU compatibility. No action needed.

## Current Status

✅ **FIXED:** Faster Whisper language parameter error  
✅ **FIXED:** STT model configuration  
✅ **LOADED:** STT "base" model (~150MB) successfully downloaded and initialized  
⚠️ **NEEDS CONFIG:** MQTT broker settings  

## Quick Configuration

### Option 1: Run Without MQTT (Testing Mode)

The application now supports running without MQTT for testing:

1. **Leave MQTT broker empty** in `config/config.yaml`:
   ```yaml
   mqtt:
     broker: ""  # Empty = MQTT disabled
   ```

2. **Configure only Porcupine access key**:
   ```yaml
   wakeword_detection:
     access_key: "YOUR_KEY_HERE"  # Get from https://console.picovoice.ai/
   ```

3. **Run Genio AI**:
   ```bash
   source genio-env/bin/activate
   python src/main.py
   ```

**What happens in test mode:**
- Wake word detection works
- Speech-to-text works
- Text-to-speech works
- No MQTT connection (local mode)
- Transcription is spoken back to you

### Option 2: Run With MQTT (Production Mode)

1. **Configure MQTT in `config/config.yaml`**:
   ```yaml
   mqtt:
     broker: "your-broker.com"  # Or IP: "192.168.1.100"
     port: 8883
     username: "your_username"
     password: "your_password"
   ```

2. **Configure Porcupine**:
   ```yaml
   wakeword_detection:
     access_key: "YOUR_KEY_HERE"
   ```

3. **Run Genio AI**:
   ```bash
   source genio-env/bin/activate
   python src/main.py
   ```

**What happens in production mode:**
- Wake word detection works
- Speech-to-text works
- Commands sent to n8n via MQTT
- Responses received and spoken

## Testing Your Setup

### Test 1: Verify STT Works
```bash
source genio-env/bin/activate
python test_stt.py
```

Expected output:
```
✅ SUCCESS! STT initialized without errors!
🎉 The language parameter fix is working correctly!
```

### Test 2: Verify Piper TTS Works
```bash
source genio-env/bin/activate
python test_piper.py
```

You should hear Swedish speech.

### Test 3: Run Full Application
```bash
source genio-env/bin/activate
python src/main.py
```

Expected startup log:
```
🤖 Initializing Genio AI...
Initializing Piper TTS...
Initializing wake word detector for 'porcupine'...
Initializing speech-to-text...
⚠️  MQTT broker not configured! MQTT features will be disabled.
✅ Genio AI initialized successfully!
```

## Understanding the Logs

### Normal Warnings (Safe to Ignore)

```
[ctranslate2] [warning] The compute type inferred from the saved model is float16...
```
**Meaning:** Model auto-converting to CPU-compatible format. This is expected and optimal.

```
⚠️  MQTT broker not configured! MQTT features will be disabled.
```
**Meaning:** Running in test mode without MQTT. Configure MQTT if you want n8n integration.

### Errors That Need Fixing

```
PORCUPINE_ACCESS_KEY is required!
```
**Fix:** Add your Porcupine access key to `config/config.yaml` or `.env`

```
TypeError: __init__(): incompatible constructor arguments
```
**Fix:** This should be fixed now. If you still see it, run `git pull` to get the latest code.

```
socket.gaierror: [Errno -2] Name or service not known
```
**Fix:** Invalid MQTT broker address. Either configure correctly or leave empty to disable MQTT.

## Configuration Files Priority

The application loads configuration in this order:

1. **Environment variables** (highest priority)
2. **`.env` file** (if exists)
3. **`config/config.yaml`** (default values)

You only need to configure ONE of these:

### Simple Setup (Recommended)
Just edit `config/config.yaml`:
```yaml
wakeword_detection:
  access_key: "YOUR_PORCUPINE_KEY"

mqtt:
  broker: ""  # Leave empty for test mode
```

### Advanced Setup
Use `.env` for sensitive data:
```bash
cp .env.example .env
nano .env
```

Add:
```env
PORCUPINE_ACCESS_KEY=your_key_here
MQTT_BROKER=your-broker.com
MQTT_USERNAME=user
MQTT_PASSWORD=pass
```

## Next Steps

1. ✅ **Get Porcupine Access Key**
   - Go to https://console.picovoice.ai/
   - Create free account
   - Copy your access key
   - Add to `config/config.yaml`

2. ⚠️ **Decide on MQTT** (Optional)
   - Test mode: Leave MQTT broker empty
   - Production: Configure your MQTT broker

3. 🚀 **Run Genio AI**
   ```bash
   source genio-env/bin/activate
   python src/main.py
   ```

4. 🎤 **Test Wake Word**
   - Say "Porcupine"
   - Listen for activation
   - Speak your command
   - Hear the response

## Troubleshooting

**Problem:** Model download is slow  
**Solution:** Be patient on first run. Model is ~150MB and caches for future use.

**Problem:** "PORCUPINE_ACCESS_KEY is required"  
**Solution:** Get free key from https://console.picovoice.ai/ and add to config.

**Problem:** MQTT connection fails  
**Solution:** Either configure correct broker or leave empty to run in test mode.

**Problem:** No audio heard  
**Solution:** Check speaker volume, verify Piper is installed: `which piper`

**Problem:** Wake word not detected  
**Solution:** Speak clearly, try different sensitivity in config (0.3-0.7)

## Support

📖 **Full Documentation:**
- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - Configuration help
- [WAKEWORD_SETUP.md](WAKEWORD_SETUP.md) - Porcupine setup
- [STT_SETUP.md](STT_SETUP.md) - Speech-to-text setup
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [FIXES_APPLIED.md](FIXES_APPLIED.md) - Recent fixes

🐛 **Still having issues?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Genio AI** 🤖 - Your intelligent Swedish voice assistant
