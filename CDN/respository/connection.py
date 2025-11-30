import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from conf import Settings


class ConnectionDB:

    def __init__(self):
        try:
            if Settings.ENV == "local":
                uri = f"mongodb://{Settings.DB_USER}:{Settings.PASSWORD}@{Settings.HOST}:27017/?authSource=admin"
            else:
                uri = f"mongodb+srv://{Settings.DB_USER}:{Settings.PASSWORD}@{Settings.HOST}/"
            self.client = MongoClient(uri)
        except:
            print("Conexion fallida al conectarse con el servidor")
    

    def get_db(self) -> Optional[Database]:
        """Obtiene la conexion si existe a la base de datos"""
        try:
            return self.client[Settings.DATABASE]
        except:
            print("Ocurrio un erro al obtener la base de datos")
            return None
