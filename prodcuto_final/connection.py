import os
from pymongo import MongoClient


PASSWORD=os.getenv("PASSWORD","mongo12345")
DB_USER=os.getenv("DB_USER","usuario_mongo")
DATABASE=os.getenv("DB","central")
HOST=os.getenv("HOST","localhost")
PORT=os.getenv("PORT","27017")
class ConnectionDB:

    def __init__(self):
        try:
            uri = f"mongodb://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/?authSource=admin&retryWrites=true&w=majority"
            self.client= client = MongoClient(uri)
        except:
            print("Conexion fallida al conectarse con el servidor")
    def get_db(self):
        try:
            return  self.client[DATABASE]
        except :
            print("Ocurrio un erro al obtener la base de datos")
            return None
