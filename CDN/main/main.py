import hashlib
import json
import os
import queue
import threading
from conf import Settings
from suscritor.subscriber import Subscriber
from respository.controller import Controller
from publicador.publisher import Publisher

mongo_controller = Controller()
suscritor = Subscriber(Settings.BROKER_HOST)
publicator = Publisher(Settings.BROKER_HOST)
suscritor.add_topic(Settings.COMMAND["QUERY"])
suscritor.add_topic(Settings.COMMAND["TOPIC"])


def data_proccesing():
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
                    res = mongo_controller.create(topic, item)
                    print(res)
        except Exception as ex:
            print(ex)


def query_proccesing():
    while True:
        if suscritor.querys.empty():
            continue
        str_json = suscritor.querys.get()
        hash_o = hashlib.sha256(str_json.encode("utf-8"))
        hash_str=hash_o.hexdigest()
        
        try:

            query = json.loads(str_json)
            topic=query.get("topic")
            topic.replace("/","_")
            res = mongo_controller.query(
                topic,
                query.get("filter"),
                query.get("order_by"),
                query.get("limit"),
                query.get("skip"),
                query.get("fields"),
            )
            data = json.dumps(res)
            publicator.publish(hash_str, data)
        except Exception as ex:
            print(ex)
            error = {
                "error": str(ex),
            }
            data = json.dumps(error)
            publicator.publish(hash_str, data)


data_proccesing_thread = threading.Thread(target=data_proccesing)
query_proccesing_thread = threading.Thread(target=query_proccesing)

data_proccesing_thread.start()
query_proccesing_thread.start()
publicator.start()
suscritor.start()
