import json
import queue
import time
from typing import Any, List

import paho.mqtt.client
import paho.mqtt.enums
import paho.mqtt.properties
import paho.mqtt.reasoncodes
from respository.controller import Controller


class Subscriber:

    def __init__(self, host):
        self.mqttc = paho.mqtt.client.Client(
            paho.mqtt.enums.CallbackAPIVersion.VERSION2
        )
        self.buffer=queue.Queue()
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        self.topics = set()
        self.mqttc.user_data_set([])
        self.host = host

    def start(self):
        self.mqttc.connect(self.host, keepalive=10)
        self.mqttc.loop_forever()

    def on_subscribe(
        self,
        client: paho.mqtt.client.Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[paho.mqtt.reasoncodes.ReasonCode],
        properties: paho.mqtt.properties.Properties,
    ) -> None:
        if reason_code_list[0].is_failure:
            print(f"Broker rejected your subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_unsubscribe(
        self,
        client: paho.mqtt.client.Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[paho.mqtt.reasoncodes.ReasonCode],
        properties: paho.mqtt.properties.Properties | None,
    ) -> None:
        if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
            print(f"Unsubscribe succeded (if SUBACK is recived in MQTTv3 it succeeded)")
        else:
            print(f"Broker replied with failure: {reason_code_list[0]}")

        client.disconnect()

    def on_message(
        self,
        client: paho.mqtt.client.Client,
        userdata: Any,
        message: paho.mqtt.client.MQTTMessage,
    ) -> None:
        """Disparador que ocurre cuando uno de los temas suscritos es recibido"""
        topic = message.topic
        payload = message.payload.decode()
        print(f"[Mensaje] Topic: {topic}  ")
        data = json.loads(payload)
        data_recibido= {"topic":topic,"data":data,"timesnap":time.time()}
        print(data_recibido)
        self.buffer.put(data_recibido)

    def on_connect(
        self,
        client: paho.mqtt.client.Client,
        userdata: Any,
        flags: paho.mqtt.client.ConnectFlags,
        reason_code: paho.mqtt.reasoncodes.ReasonCode,
        properties: paho.mqtt.properties.Properties | None,
    ) -> None:
        """Disparador que ocurre cuando s inicia una conxion"""
        if reason_code.is_failure:
            print(
                f"Failed to connect {reason_code}. loop_forever() will retry connection"
            )
        else:
            for t in self.topics:
                client.subscribe(t)
                print(f"[on_connect] Suscrito: {t}")

    def add_topic(self, topic: str, qos: int = 0):
        """Agrega un topic a la lista de topic y crea la suscripcion a el"""
        try:
            if topic not in self.topics:
                self.topics.add(topic)
                self.mqttc.subscribe(topic, qos)
                print(f"Suscrito  : {topic}")
            else:
                print(f"El topic '{topic}' ya está suscrito.")
        except Exception as ex:
            print(ex)
