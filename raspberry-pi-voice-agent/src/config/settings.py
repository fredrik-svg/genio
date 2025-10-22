# Configuration settings for the voice agent application
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from YAML file
config_file = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# Porcupine Wake Word settings
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY', '')
WAKE_WORD = os.getenv('WAKE_WORD') or config.get('wakeword_detection', {}).get('keyword', 'porcupine')
WAKE_WORD_MODEL_PATH = os.getenv('WAKE_WORD_MODEL_PATH') or config.get('wakeword_detection', {}).get('model_path', '')
WAKE_WORD_SENSITIVITY = float(os.getenv('WAKE_WORD_SENSITIVITY', '0.5'))

# Speech-to-Text settings
STT_MODEL_PATH = os.getenv('STT_MODEL_PATH') or config.get('stt', {}).get('model_path', 'path/to/faster_whisper/model')
STT_LANGUAGE = os.getenv('STT_LANGUAGE') or config.get('stt', {}).get('language', 'sv')
STT_MODEL = STT_MODEL_PATH  # Alias for backward compatibility

# Text-to-Speech settings
TTS_ENGINE = config.get('tts', {}).get('engine', 'piper')
TTS_LANGUAGE = os.getenv('TTS_LANGUAGE') or config.get('tts', {}).get('language', 'sv')
TTS_VOICE = config.get('tts', {}).get('voice', 'sv_SE-nst-medium')
TTS_MODEL_PATH = os.getenv('TTS_MODEL_PATH') or config.get('tts', {}).get('model_path', 'models/sv_SE-nst-medium.onnx')
TTS_CONFIG_PATH = os.getenv('TTS_CONFIG_PATH') or config.get('tts', {}).get('config_path', 'models/sv_SE-nst-medium.onnx.json')
TTS_MODEL = TTS_MODEL_PATH  # Alias for backward compatibility

# MQTT settings
MQTT_BROKER = os.getenv('MQTT_BROKER') or config.get('mqtt', {}).get('broker', 'mqtt.example.com')
MQTT_PORT = int(os.getenv('MQTT_PORT', '8883')) if os.getenv('MQTT_PORT') else config.get('mqtt', {}).get('port', 8883)
MQTT_TOPIC = os.getenv('MQTT_TOPIC') or config.get('mqtt', {}).get('topic', 'genio/agent')
MQTT_CLIENT_ID = config.get('mqtt', {}).get('client_id', 'genio_ai')
MQTT_USERNAME = os.getenv('MQTT_USERNAME') or config.get('mqtt', {}).get('username', '')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD') or config.get('mqtt', {}).get('password', '')

# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL') or config.get('logging', {}).get('level', 'INFO')
LOG_FILE = os.getenv('LOG_FILE') or config.get('logging', {}).get('file', 'logs/genio_ai.log')

# Configuration parameters
CONFIG_PARAMS = {
    "volume": 1.0,  # Volume level for TTS output (0.0 to 1.0)
    "wake_word_sensitivity": 0.5,  # Sensitivity for wake word detection (0.0 to 1.0)
}