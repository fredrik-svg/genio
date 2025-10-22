# Configuration settings for the voice agent application
import yaml
from pathlib import Path

# Load configuration from YAML file
config_file = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# Wake word detection settings
WAKE_WORD = config.get('wakeword_detection', {}).get('keyword', 'hej')
WAKE_WORD_MODEL_PATH = config.get('wakeword_detection', {}).get('model_path', 'path/to/porcupine/model.pv')

# Speech-to-Text settings
STT_MODEL_PATH = config.get('stt', {}).get('model_path', 'path/to/faster_whisper/model')
STT_LANGUAGE = config.get('stt', {}).get('language', 'sv')
STT_MODEL = STT_MODEL_PATH  # Alias for backward compatibility

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

# Logging settings
LOG_LEVEL = config.get('logging', {}).get('level', 'INFO')
LOG_FILE = config.get('logging', {}).get('file', 'logs/genio_ai.log')

# Configuration parameters
CONFIG_PARAMS = {
    "volume": 1.0,  # Volume level for TTS output (0.0 to 1.0)
    "wake_word_sensitivity": 0.5,  # Sensitivity for wake word detection (0.0 to 1.0)
}