import platform
import socket
import os
import time
import psutil
 
 
def get_metadata():
    metadata = {
        "topic":"PC/Temperatura",
        "so": platform.system(),
        "version_so": platform.version(),
        "release": platform.release(),
        "arquitectura": platform.machine(),
        "procesador": platform.processor(),
        "nombre_equipo": socket.gethostname(),
        "usuario_actual": os.getlogin(),
        "cpu_fisica": psutil.cpu_count(logical=False),
        "cpu_logica": psutil.cpu_count(logical=True),
        "ram_total":psutil.virtual_memory()
    }
    return metadata
def get_temperature():
    temps = psutil.sensors_temperatures()
    return temps
def get_datos():
    datos = {
        "timestamp": int(time.time()),
        "metadata": get_metadata(),
        "temperature": get_temperature()
    }
    return datos