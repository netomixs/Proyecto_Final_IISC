import hashlib
import json
import os
from kax import acts
from kax import mem
import time
import time
from typing import Any

import paho.mqtt.client
import paho.mqtt.enums
import paho.mqtt.reasoncodes
import paho.mqtt.properties
from generar_datos import get_datos

 
def on_publish(
    client: paho.mqtt.client.Client,
    userdata: Any,
    mid: int,
    reason_code: paho.mqtt.reasoncodes.ReasonCode,
    properties: paho.mqtt.properties.Properties | None
) -> None:
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    try:
        userdata.remove(mid)
    except KeyError:
        print('on_publish() is called with a mid not present in unacked_publish')
        print('This is due to an unavoidable race-condition:')
        print('* publish() return the mid of the message sent.')
        print('* mid from publish() is added to unacked_publish by the main thread')
        print('* on_publish() is called by the loop_start thread')
        print('While unlikely (because on_publish() will be called after a network round-trip),')
        print(' this is a race-condition that COULD happen')
        print('')
        print('The best solution to avoid race-condition is using the msg_info from publish()')
        print('We could also try using a list of acknowledged mid rather than removing from pending list,')
        print('but remember that mid could be re-used !')          
unpacked_publish = set()
mqttc = paho.mqtt.client.Client(paho.mqtt.enums.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish
msg_info = mqttc.publish("paho/test/topic", "my message", qos=1)                            

mqttc.user_data_set(unpacked_publish)
mqttc.connect('localhost', keepalive=10)
mqttc.loop_start()

tabla_hash=""
def get_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def put_in_shm(data, hash):
    data = json.dumps(data)
    size = len(data)
    acts.makeShm(hash, size)
    acts.putDataToShm(hash, data)


def cargar_datos():
    datos = get_datos()
    clave = get_hash(datos)
    put_in_shm(datos, clave)
    put_clave(clave, datos["metadata"]["topic"])
    return clave


def put_clave(clave, name):
    dict_claves = get_tabla_hash()
    dict_claves[clave] = {"tag":name,"last":int(time.time())}
    try:
        acts.removeShm(tabla_hash)
    except:
        pass
    put_in_shm( dict_claves,tabla_hash)


def get_tabla_hash():
    try:
        res = acts.getRes(tabla_hash)
        dict_claves = eval(res)
        return dict_claves
    except:
        return {}

while True:
    data= get_datos()
    print(data)
    msg_info = mqttc.publish("pc/temperatura",json.dumps( data), qos=1)
    unpacked_publish.add(msg_info.mid)
    while len(unpacked_publish):
        time.sleep(0.1)
    msg_info.wait_for_publish()
    time.sleep(10)

 
