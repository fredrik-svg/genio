import paho.mqtt.client as mqtt
from config.settings import (
    MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD,
    PORCUPINE_ACCESS_KEY, WAKE_WORD, WAKE_WORD_MODEL_PATH, WAKE_WORD_SENSITIVITY,
    STT_MODEL_PATH, TTS_MODEL_PATH, TTS_CONFIG_PATH, TTS_LANGUAGE
)
from audio.microphone import Microphone
from audio.speaker import Speaker
from wakeword.porcupine_detector import PorcupineDetector
from stt.faster_whisper import FasterWhisper
from tts.tts_engine import PiperTTS
from utils.logger import Logger

class GenioAI:
    def __init__(self):
        self.logger = Logger()
        self.logger.info("🤖 Initializing Genio AI...")
        
        # Validate Porcupine access key
        if not PORCUPINE_ACCESS_KEY:
            raise ValueError(
                "PORCUPINE_ACCESS_KEY is required! "
                "Add it to config/config.yaml or .env file. "
                "Get free key from: https://console.picovoice.ai/"
            )
        
        self.mqtt_client = mqtt.Client()
        self.microphone = Microphone()
        
        # Initialize Piper TTS
        self.logger.info("Initializing Piper TTS...")
        self.tts = PiperTTS(
            model_path=TTS_MODEL_PATH,
            config_path=TTS_CONFIG_PATH,
            language=TTS_LANGUAGE
        )
        self.speaker = Speaker(self.tts)
        
        # Initialize Porcupine wake word detector
        self.logger.info(f"Initializing wake word detector for '{WAKE_WORD}'...")
        if WAKE_WORD_MODEL_PATH:
            # Use custom .ppn file
            self.porcupine_detector = PorcupineDetector(
                access_key=PORCUPINE_ACCESS_KEY,
                keyword_paths=[WAKE_WORD_MODEL_PATH],
                sensitivity=WAKE_WORD_SENSITIVITY
            )
        else:
            # Use built-in keyword
            self.porcupine_detector = PorcupineDetector(
                access_key=PORCUPINE_ACCESS_KEY,
                keywords=[WAKE_WORD],
                sensitivity=WAKE_WORD_SENSITIVITY
            )
        
        # Initialize STT
        self.logger.info("Initializing speech-to-text...")
        self.stt = FasterWhisper(STT_MODEL_PATH)

        self.setup_mqtt()
        self.logger.info("✅ Genio AI initialized successfully!")

    def setup_mqtt(self):
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
        # Set username and password if provided
        if MQTT_USERNAME and MQTT_PASSWORD:
            self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Genio AI connected to MQTT broker")
        client.subscribe("genio/commands")

    def on_message(self, client, userdata, msg):
        command = msg.payload.decode()
        self.logger.info(f"Received command: {command}")
        self.process_command(command)

    def process_command(self, command):
        # Process the command and respond accordingly
        response = self.stt.convert(command)
        self.speaker.speak(response)

    def listen_for_wake_word(self):
        while True:
            if self.porcupine_detector.detect():
                self.logger.info("Wake word detected!")
                audio = self.microphone.listen()
                command = self.stt.transcribe(audio)
                self.mqtt_client.publish("genio/commands", command)

    def run(self):
        self.listen_for_wake_word()

if __name__ == "__main__":
    agent = GenioAI()
    agent.run()