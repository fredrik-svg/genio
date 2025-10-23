# Configuration settings for the voice agent application
import yaml
import os
from pathlib import Path

# Load configuration from YAML file
config_file = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# Porcupine Wake Word settings
PORCUPINE_ACCESS_KEY = config.get('wakeword_detection', {}).get('access_key', '')
if not PORCUPINE_ACCESS_KEY or PORCUPINE_ACCESS_KEY == "YOUR_PORCUPINE_ACCESS_KEY_HERE":
    print("⚠️  VARNING: PORCUPINE_ACCESS_KEY är inte konfigurerad!")
    print("   Lägg till i config/config.yaml")
    print("   Skaffa gratis key: https://console.picovoice.ai/")
    
WAKE_WORD = config.get('wakeword_detection', {}).get('keyword', 'porcupine')
WAKE_WORD_MODEL_PATH = config.get('wakeword_detection', {}).get('model_path', '')
WAKE_WORD_SENSITIVITY = config.get('wakeword_detection', {}).get('sensitivity', 0.5)

# Speech-to-Text settings
STT_MODEL_SIZE = config.get('stt', {}).get('model_size', 'base')
STT_LANGUAGE = config.get('stt', {}).get('language', 'sv')
# Legacy support for model_path (if someone still uses it)
STT_MODEL_PATH = config.get('stt', {}).get('model_path', STT_MODEL_SIZE)
STT_MODEL = STT_MODEL_SIZE  # Alias for backward compatibility

# Text-to-Speech settings
TTS_ENGINE = config.get('tts', {}).get('engine', 'piper')
TTS_LANGUAGE = config.get('tts', {}).get('language', 'sv')
TTS_VOICE = config.get('tts', {}).get('voice', 'sv_SE-nst-medium')
TTS_MODEL_PATH = config.get('tts', {}).get('model_path', 'models/sv_SE-nst-medium.onnx')
TTS_CONFIG_PATH = config.get('tts', {}).get('config_path', 'models/sv_SE-nst-medium.onnx.json')
TTS_MODEL = TTS_MODEL_PATH  # Alias for backward compatibility

# MQTT settings
MQTT_BROKER = config.get('mqtt', {}).get('broker', 'mqtt.example.com')
MQTT_PORT = config.get('mqtt', {}).get('port', 8883)
MQTT_TOPIC = config.get('mqtt', {}).get('topic', 'genio/agent')
MQTT_CLIENT_ID = config.get('mqtt', {}).get('client_id', 'genio_ai')
MQTT_USERNAME = config.get('mqtt', {}).get('username', '')
MQTT_PASSWORD = config.get('mqtt', {}).get('password', '')
MQTT_USE_TLS = config.get('mqtt', {}).get('use_tls', True)

# Warn about placeholder values
if MQTT_BROKER in ["YOUR_MQTT_BROKER_ADDRESS", "mqtt.example.com"]:
    print("⚠️  VARNING: MQTT_BROKER har inte ändrats från exempel-värdet!")
    print("   Uppdatera config/config.yaml med din riktiga broker-adress")
if MQTT_USERNAME in ["YOUR_MQTT_USERNAME", ""] or MQTT_PASSWORD in ["YOUR_MQTT_PASSWORD", ""]:
    print("⚠️  VARNING: MQTT credentials är inte konfigurerade!")
    print("   Uppdatera config/config.yaml med username och password")

# Audio settings
AUDIO_RECORD_SECONDS = config.get('audio', {}).get('record_seconds', 5)

# Logging settings
LOG_LEVEL = config.get('logging', {}).get('level', 'INFO')
LOG_FILE = config.get('logging', {}).get('file', 'logs/genio_ai.log')

# Configuration parameters
CONFIG_PARAMS = {
    "volume": 1.0,  # Volume level for TTS output (0.0 to 1.0)
    "wake_word_sensitivity": 0.5,  # Sensitivity for wake word detection (0.0 to 1.0)
}