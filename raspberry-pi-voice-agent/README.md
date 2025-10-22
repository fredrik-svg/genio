````markdown
# Genio AI 🤖

> An intelligent voice assistant for Raspberry Pi with Swedish language support

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](ht## Documentation

- 📖 **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - Guide för konfiguration med config.yaml
- 🚀 **[QUICKSTART.md](QUICKSTART.md)** - Snabbstart och testning
- 🔧 **[INSTALLATION.md](INSTALLATION.md)** - Detaljerad installationsguide med lösningar för vanliga problem
- 🎤 **[WAKEWORD_SETUP.md](WAKEWORD_SETUP.md)** - Guide för Porcupine wake word setup
- 🎙️ **[STT_SETUP.md](STT_SETUP.md)** - Guide för Faster Whisper speech-to-text setup
- 🔊 **[PIPER_INSTALLATION.md](PIPER_INSTALLATION.md)** - Guide för Piper TTS-installation
- ☁️ **[HIVEMQ_SETUP.md](HIVEMQ_SETUP.md)** - HiveMQ Cloud MQTT konfiguration och testning
- 🆘 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Felsökning och lösningar
- 🎨 **[REBRANDING.md](REBRANDING.md)** - Information om Genio AI-namnbytet
- 📝 **[CHANGELOG_PIPER.md](CHANGELOG_PIPER.md)** - Versionshistorik och ändringarpython.org/downloads/)
[![Piper TTS](https://img.shields.io/badge/TTS-Piper-green.svg)](https://github.com/rhasspy/piper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview
Genio AI is an intelligent voice agent running on a Raspberry Pi 5, designed to interact with an n8n workflow. The application utilizes various technologies for voice recognition and synthesis, including wake word detection, speech-to-text, and text-to-speech functionalities.

## Features
- **Wake Word Detection**: Utilizes Porcupine for detecting a specific wake word.
- **Speech-to-Text**: Integrates Faster Whisper for converting spoken language into text.
- **Text-to-Speech**: Uses Piper TTS for high-quality, local neural text-to-speech synthesis.
- **MQTT Communication**: Communicates with an n8n workflow via MQTT protocol (port 8883 with TLS/SSL support).
- **Swedish Language Support**: The application is configured to operate in Swedish.
- **Offline Capable**: Works completely offline after initial setup.

## Project Structure
```
genio-ai
├── src
│   ├── main.py                # Genio AI entry point
│   ├── config                 # Configuration settings
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── audio                  # Audio input/output handling
│   │   ├── __init__.py
│   │   ├── microphone.py
│   │   └── speaker.py
│   ├── wakeword               # Wake word detection
│   │   ├── __init__.py
│   │   └── porcupine_detector.py
│   ├── stt                    # Speech-to-text processing
│   │   ├── __init__.py
│   │   └── faster_whisper.py
│   ├── tts                    # Text-to-speech functionality
│   │   ├── __init__.py
│   │   └── tts_engine.py
│   ├── mqtt                   # MQTT client management
│   │   ├── __init__.py
│   │   └── client.py
│   └── utils                  # Utility functions
│       ├── __init__.py
│       └── logger.py
├── config
│   └── config.yaml            # Genio AI configuration parameters
├── models
│   └── .gitkeep               # Keeps the models directory in version control
├── requirements.txt           # Project dependencies
├── test_piper.py              # Piper TTS test script
├── PIPER_INSTALLATION.md      # Detailed Piper installation guide
└── README.md                  # Project documentation
```

## Installation

### Snabbinstallation (Rekommenderat)

```bash
# 1. Klona repository
git clone https://github.com/fredrik-svg/genio.git
cd genio/raspberry-pi-voice-agent

# 2. Kör installationsscript
chmod +x install.sh
./install.sh

# 3. Aktivera virtuell miljö
source genio-env/bin/activate

# 4. Konfigurera applikationen
nano config/config.yaml  # Redigera MQTT-inställningar etc.

# 5. Testa installation
python test_piper.py

# 6. Kör Genio AI
python src/main.py
```

### Manuell installation

Om du får felet `error: externally-managed-environment`:

1. Clone the repository:
   ```bash
   git clone https://github.com/fredrik-svg/genio.git
   cd genio/raspberry-pi-voice-agent
   ```

2. **Skapa virtuell miljö (VIKTIGT för att undvika "externally-managed-environment" fel):**
   ```bash
   python3 -m venv genio-env
   source genio-env/bin/activate
   ```

3. Install Piper TTS:
   ```bash
   # Install Piper on Raspberry Pi
   wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
   tar -xzf piper_arm64.tar.gz
   sudo mv piper/piper /usr/local/bin/
   sudo chmod +x /usr/local/bin/piper
   ```

4. Download Swedish voice model for Piper:
   ```bash
   # Create models directory
   mkdir -p models
   
   # Download Swedish voice model
   cd models
   wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx
   wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json
   cd ..
   ```

5. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurera applikationen:**

   Redigera config.yaml och ändra placeholder-värdena till dina riktiga värden:
   ```bash
   nano config/config.yaml
   ```
   
   Ändra dessa värden:
   ```yaml
   wakeword_detection:
     access_key: "din_porcupine_key"  # Ändra från YOUR_PORCUPINE_ACCESS_KEY_HERE
                                       # Från https://console.picovoice.ai/
   
   mqtt:
     broker: "din-broker.com"          # Ändra från YOUR_MQTT_BROKER_ADDRESS
     port: 8883
     username: "ditt_användarnamn"    # Ändra från YOUR_MQTT_USERNAME
     password: "ditt_lösenord"        # Ändra från YOUR_MQTT_PASSWORD
   ```

   Se [CONFIG_GUIDE.md](CONFIG_GUIDE.md) för mer information om konfiguration.

5. Test wake word detection:
   ```bash
   python test_wakeword.py
   ```

7. Run the application:
   ```bash
   python src/main.py
   ```

## Usage
Once Genio AI is running, it will listen for the specified wake word. Upon detection, it will process the audio input, convert it to text, and interact with the n8n workflow via MQTT. Responses will be converted to speech and played back through the speaker.

### Basic Workflow
1. Say the wake word (e.g., "Hej")
2. Genio AI activates and listens
3. Speak your command
4. Command is sent to n8n via MQTT
5. Response is spoken back using Piper TTS

## Documentation

- 📖 **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - Guide för konfiguration med config.yaml
- 🚀 **[QUICKREF.md](QUICKREF.md)** - Snabbreferens för daglig användning
- 🔧 **[INSTALLATION.md](INSTALLATION.md)** - Detaljerad installationsguide med lösningar för vanliga problem
- 🎤 **[WAKEWORD_SETUP.md](WAKEWORD_SETUP.md)** - Guide för Porcupine wake word setup
- � **[PIPER_INSTALLATION.md](PIPER_INSTALLATION.md)** - Guide för Piper TTS-installation
- 🆘 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Felsökning och lösningar
- 🎨 **[REBRANDING.md](REBRANDING.md)** - Information om Genio AI-namnbytet
- 📝 **[CHANGELOG_PIPER.md](CHANGELOG_PIPER.md)** - Versionshistorik och ändringar

## Troubleshooting

### "externally-managed-environment" error
This is a common issue on modern Linux systems. **Solution:** Use a virtual environment:
```bash
python3 -m venv genio-env
source genio-env/bin/activate
pip install -r requirements.txt
```

### MQTT Connection Issues
- **HiveMQ Cloud:** Verify credentials in `config/config.yaml`
- Check port 8883 is open and TLS is enabled
- Test connection: `python test_mqtt.py`
- See [HIVEMQ_SETUP.md](HIVEMQ_SETUP.md) for detailed HiveMQ configuration

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more troubleshooting help.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.