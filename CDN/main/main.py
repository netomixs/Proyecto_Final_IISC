import queue
import threading
from suscritor.subscriber import Subscriber
from respository.controller import Controller

BATCH_SIZE = 100
suscritor = Subscriber("localhost")

suscritor.add_topic("pc/numer_process")
suscritor.add_topic("pc/cpu_temp_avg")
suscritor.add_topic("pc/cpu_usage_avg")

mongo = Controller()

if mongo is None:
    raise Exception(" No se puede acceder a ala base de datos")

def mongo_procees():
     """Se encarga de publicar los datos recibidos a mongoDB"""
     while True:
        if suscritor.buffer.empty():
            continue
        documentos = suscritor.buffer.get()
        try:
            topic = documentos["topic"]
            data = documentos["data"]
            if len(data) > 0:
                for item in data:
                   res= mongo.create(topic, item)
                   print(res)
        except Exception as ex:
            print(ex)


mongo_thread = threading.Thread(target=mongo_procees)
mongo_thread.start()
suscritor.start()
