import os
import time
import time
from typing import Any
import paho.mqtt.client
import paho.mqtt.enums
import paho.mqtt.reasoncodes
import paho.mqtt.properties
from generar_datos import get_datos

HOST = os.getenv('HOST', 'localhost')
class Publisher:
        def __init__(self):
            try:
                self.unpacked_publish = set()
                self.mqttc = paho.mqtt.client.Client(paho.mqtt.enums.CallbackAPIVersion.VERSION2)
                self.mqttc.on_publish = self.on_publish
                self.mqttc.user_data_set(self.unpacked_publish)
                self.mqttc.connect(HOST, keepalive=10)
                self.mqttc.loop_start()
            except Exception as ex:
                 print(ex)

        def on_publish(self,
            client: paho.mqtt.client.Client,
            userdata: Any,
            mid: int,
            reason_code: paho.mqtt.reasoncodes.ReasonCode,
            properties: paho.mqtt.properties.Properties | None
        ) -> None:
            print(f" Mensaje publicado (mid={mid})")
        def publish(self,topic,data):
            msg_info = self.mqttc.publish(topic, data, qos=1)
            msg_info.wait_for_publish()







 

 
