# Raspberry Pi Voice Agent

## Overview
This project implements a voice agent running on a Raspberry Pi 5, designed to interact with an n8n workflow. The application utilizes various technologies for voice recognition and synthesis, including wake word detection, speech-to-text, and text-to-speech functionalities.

## Features
- **Wake Word Detection**: Utilizes Porcupine for detecting a specific wake word.
- **Speech-to-Text**: Integrates Faster Whisper for converting spoken language into text.
- **Text-to-Speech**: Uses Piper TTS for high-quality, local neural text-to-speech synthesis.
- **MQTT Communication**: Communicates with an n8n workflow via MQTT protocol.
- **Swedish Language Support**: The application is configured to operate in Swedish.

## Project Structure
```
raspberry-pi-voice-agent
├── src
│   ├── main.py                # Entry point of the application
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
│   └── config.yaml            # Configuration parameters in YAML format
├── models
│   └── .gitkeep               # Keeps the models directory in version control
├── requirements.txt           # Project dependencies
├── .env.example               # Example environment variables
└── README.md                  # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd raspberry-pi-voice-agent
   ```

2. Install Piper TTS:
   ```bash
   # Install Piper on Raspberry Pi
   wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
   tar -xzf piper_arm64.tar.gz
   sudo mv piper/piper /usr/local/bin/
   sudo chmod +x /usr/local/bin/piper
   ```

3. Download Swedish voice model for Piper:
   ```bash
   # Create models directory
   mkdir -p models
   
   # Download Swedish voice model
   cd models
   wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx
   wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json
   cd ..
   ```

4. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure the application by editing `config/config.yaml` to set your desired parameters.

6. Run the application:
   ```
   python src/main.py
   ```

## Usage
Once the application is running, it will listen for the specified wake word. Upon detection, it will process the audio input, convert it to text, and interact with the n8n workflow via MQTT. Responses will be converted to speech and played back through the speaker.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.