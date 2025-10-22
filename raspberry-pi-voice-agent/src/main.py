import paho.mqtt.client as mqtt
from config.settings import MQTT_BROKER, MQTT_PORT, WAKE_WORD, STT_MODEL, TTS_MODEL
from audio.microphone import Microphone
from audio.speaker import Speaker
from wakeword.porcupine_detector import PorcupineDetector
from stt.faster_whisper import FasterWhisper
from tts.tts_engine import TTS
from utils.logger import Logger

class VoiceAgent:
    def __init__(self):
        self.logger = Logger()
        self.mqtt_client = mqtt.Client()
        self.microphone = Microphone()
        self.speaker = Speaker()
        self.porcupine_detector = PorcupineDetector(WAKE_WORD)
        self.stt = FasterWhisper(STT_MODEL)
        self.tts = TTS(TTS_MODEL)

        self.setup_mqtt()

    def setup_mqtt(self):
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected to MQTT broker")
        client.subscribe("voice/commands")

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
                self.mqtt_client.publish("voice/commands", command)

    def run(self):
        self.listen_for_wake_word()

if __name__ == "__main__":
    agent = VoiceAgent()
    agent.run()