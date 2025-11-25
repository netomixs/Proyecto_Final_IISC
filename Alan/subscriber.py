from typing import Any, List

import paho.mqtt.client
import paho.mqtt.enums
import paho.mqtt.properties
import paho.mqtt.reasoncodes


def on_subscribe(
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
    client: paho.mqtt.client.Client,
    userdata: Any,
    message: paho.mqtt.client.MQTTMessage,
) -> None:
    message.payload


def on_connect(
    client: paho.mqtt.client.Client,
    userdata: Any,
    flags: paho.mqtt.client.ConnectFlags,
    reason_code: paho.mqtt.reasoncodes.ReasonCode,
    properties: paho.mqtt.properties.Properties | None,
) -> None:
    if reason_code.is_failure:
        print(f"Failed to connect {reason_code}. loop_forever() will retry connection")
    else:
        client.subscribe("#")


mqttc = paho.mqtt.client.Client(paho.mqtt.enums.CallbackAPIVersion.VERSION2)
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_unsubscribe = on_unsubscribe

mqttc.user_data_set([])
mqttc.connect("localhost", keepalive=10)
mqttc.loop_forever()

print(mqttc.user_data_get())
