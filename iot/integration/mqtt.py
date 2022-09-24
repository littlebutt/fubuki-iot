from typing import Callable, Any

from paho.mqtt import publish, subscribe
from paho.mqtt.client import Client, MQTTMessage

MQTT_UserData = Any

MQTT_Client = Client

MQTT_Message = MQTTMessage

MQTT_Callback = Callable[[MQTT_Client, MQTT_UserData, MQTT_Message], None]


class MQTTClient:

    def __init__(self, hostname: str = '127.0.0.1', port: int = 1883):
        self.hostname = hostname
        self.port = port

    def publish(self, topic: str, payload: str):
        publish.single(topic=topic, payload=payload, hostname=self.hostname, port=self.port)

    def subscribe(self, topics: str, callback: MQTT_Callback):
        subscribe.callback(topics=topics, callback=callback, hostname=self.hostname, port=self.port)