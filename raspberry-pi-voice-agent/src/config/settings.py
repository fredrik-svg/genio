# Configuration settings for the voice agent application

# Wake word detection settings
WAKE_WORD = "hej dator"  # The wake word to listen for
WAKE_WORD_MODEL_PATH = "path/to/porcupine/model.pv"  # Path to the Porcupine model file

# Speech-to-Text settings
STT_MODEL_PATH = "path/to/faster_whisper/model"  # Path to the Faster Whisper model
STT_LANGUAGE = "sv"  # Language for STT (Swedish)

# Text-to-Speech settings
TTS_ENGINE = "pyttsx3"  # Suggested TTS engine (e.g., pyttsx3)
TTS_LANGUAGE = "sv"  # Language for TTS (Swedish)

# MQTT settings
MQTT_BROKER = "mqtt.example.com"  # MQTT broker address
MQTT_PORT = 1883  # MQTT broker port
MQTT_TOPIC = "voice/agent"  # Topic for communication
MQTT_CLIENT_ID = "raspberry_pi_voice_agent"  # Unique client ID for MQTT connection

# Configuration parameters
CONFIG_PARAMS = {
    "volume": 1.0,  # Volume level for TTS output (0.0 to 1.0)
    "wake_word_sensitivity": 0.5,  # Sensitivity for wake word detection (0.0 to 1.0)
}