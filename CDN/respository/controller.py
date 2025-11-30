from bson import ObjectId
from respository.connection import ConnectionDB


class Controller:
    def __init__(self):
        conexion = ConnectionDB()
        self.db = conexion.get_db()
        if self.db is None:
            raise Exception("No se puede acceder a la base de datos")

    def create(self, tabla, data):
        try:
            colection = self.db[tabla]
            result = colection.insert_one(data)
            return result
        except Exception as ex:
            print(ex)
            return None

    def update(self, tabla, id, data):
        try:
            collection = self.db[tabla]
            result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            return result
        except:
            return None

    def get_by_id(self, tabla, id):
        collection = self.db[tabla]
        doc = collection.find_one({"_id": ObjectId(id)})

        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def query(
        self, tabla, filtros=None, ordenar=None, limite=None, saltar=None, campos=None
    ):
        collection = self.db[tabla]
        filtros = filtros or {}
        cursor = collection.find(filtros, campos)

        if ordenar:
            cursor = cursor.sort(ordenar)

        if saltar:
            cursor = cursor.skip(saltar)

        if limite:
            cursor = cursor.limit(limite)
        resultados = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            resultados.append(doc)

        return resultados
