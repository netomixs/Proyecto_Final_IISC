import hashlib
import json
import os
from kax import acts
from kax import mem
import time
import sys
import psutil
import platform
from generar_datos import get_datos

objetivos = "consumo_archivos1/"
save_path = "archivos/"
acts.setUrl("http://148.247.201.210:5060/api")
acts.setStorageUrl("http://148.247.201.210:5070/api")
acts.setBrokerPort(1883)
acts.setBrokerUrl("148.247.201.226")

tabla_hash = "tabla_claves"


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

acts.removeShm(tabla_hash)
while True:
    cargar_datos()
    print(get_tabla_hash())
    time.sleep(10)
