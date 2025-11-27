import os
from pymongo import MongoClient


PASSWORD=os.getenv("PASSWORD","mongo12345")
DB_USER=os.getenv("DB_USER","usuario_mongo")
DATABASE=os.getenv("DB","central")
HOST=os.getenv("HOST","localhost")
ENV = os.getenv("ENV", "local") 
class ConnectionDB:

    def __init__(self):
        try:
            if ENV == "local":
                uri = f"mongodb://{DB_USER}:{PASSWORD}@{HOST}:27017/?authSource=admin"
            else:
                uri = f"mongodb+srv://{DB_USER}:{PASSWORD}@{HOST}/"
            self.client = MongoClient(uri)
        except:
            print("Conexion fallida al conectarse con el servidor")
    def get_db(self):
        try:
            return  self.client[DATABASE]
        except :
            print("Ocurrio un erro al obtener la base de datos")
            return None
