import json
from typing import ClassVar

from iot.integration.mqtt import MQTTClient, MQTT_Callback
from iot.models import FunctionDeviceModel


class MessagesProcessor:
    __client: ClassVar["MQTTClient"] = None

    def __init__(self, hostname: str, port: int):
        self.__client = MQTTClient(hostname=hostname, port=port)

    def publish(self, model: FunctionDeviceModel):
        data = model.data if model.is_raw else json.dumps(model.data)
        self.__client.publish(topic=model.topic, payload=data)

    def subscribe(self, topics: str, callback: MQTT_Callback):
        self.__client.subscribe(topics=topics, callback=callback)

# mqttx-cli-win-x64.exe sub -t default/light  -p 1883
# mqttx-cli-win-x64.exe pub -t self/button -p 1883 -m {\"topic\":\"self/button\",\"device\":\"button\",\"verbose\":\"false\",\"message\":\"有人按下了按钮\"}
