from datetime import datetime
import platform
import socket
import os
import threading
import time
import psutil
import os
import glob


def get_metadata():
    metadata = {
        "topic": "PC/Temperatura",
        "so": platform.system(),
        "version_so": platform.version(),
        "release": platform.release(),
        "arquitectura": platform.machine(),
        "procesador": platform.processor(),
        "nombre_equipo": socket.gethostname(),
        "usuario_actual": os.getlogin(),
    }
    return metadata


def get_temperature():
    temps = psutil.sensors_temperatures()
    return temps


def get_datos():
    datos = {
        "timestamp": int(time.time()),
        "metadata": get_metadata(),
        "temperature": get_temperature(),
    }
    return datos


def get_cpu_average_temperature():
    nucleo_name = "coretemp"
    temperatura = get_temperature()
    if nucleo_name not in temperatura:
        raise Exception("No se puede acceder a la temperatura del nucleo")
    nucleo = temperatura[nucleo_name]
    sytem=nucleo[0]
    if sytem[0] == "Package id 0":
            return sytem[1]
    raise Exception("Temperatura no localizada")


def get_cpu_avarage_usage(intervalo=1):
    usos = psutil.cpu_percent(interval=intervalo, percpu=True)
    return sum(usos) / len(usos)


def get_num_process():
    return len(psutil.pids())


def get_num_process_serie(interection, intervalo):
    resultados = []
    for i in range(0, interection):
        resultados.append(
            {
                "timestamp": datetime.now().isoformat(),
                "num_process": get_num_process(),
            }
        )
        time.sleep(intervalo)
    return resultados


def get_cpu_avarge_temperature_serie(interection, intervalo):
    resultados = []
    for i in range(0, interection):
        resultados.append(
            {
                "timestamp": datetime.now().isoformat(),
                "cpu_temperature_avarage": get_cpu_average_temperature(),
            }
        )
        time.sleep(intervalo)
    return resultados


def get_cpu_avarage_usage_serie(interection, intervalo):
    resultados = []
    for i in range(0, interection):
        resultados.append(
            {
                "timestamp": datetime.now().isoformat(),
                "cpu_usage_avarage": get_cpu_avarage_usage(),
            }
        )
        time.sleep(intervalo)
    return resultados



