import json
import threading
import time
from generar_datos import get_datos
from generar_datos import get_cpu_avarage_usage_serie
from generar_datos import get_cpu_avarge_temperature_serie
from generar_datos import get_num_process_serie
from publisher import Publisher
publicador= Publisher()

def preprocess_data(data):
    print(data)
    return json.dumps(data)
def get_series():
    num = 10
 

    def proces_proces():
        while True:
            data  = get_num_process_serie(num, 1)
            data=preprocess_data(data)
            publicador.publish("pc/numer_process",data)
            time.sleep(1)
    def process_temperature():
        while True:
            data = get_cpu_avarge_temperature_serie(num, 1)
            data=preprocess_data(data)
            publicador.publish("pc/cpu_temp_avg",data)
            time.sleep(1)
    def process_use_cpu():
        while True:
            data = get_cpu_avarage_usage_serie(num, 1)
            data=preprocess_data(data)
            publicador.publish("pc/cpu_usage_avg",data)
            time.sleep(1)
    t1 = threading.Thread(target=proces_proces)
    t2 = threading.Thread(target=process_temperature)
    t3 = threading.Thread(target=process_use_cpu)

    t1.start()
    t2.start()
    t3.start()

get_series()