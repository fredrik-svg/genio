import paho.mqtt.client as mqtt
import json
from config.settings import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        self.client.subscribe(MQTT_TOPIC)

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        print(f"Received message: {payload}")

    def publish(self, message):
        self.client.publish(MQTT_TOPIC, json.dumps(message))

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()