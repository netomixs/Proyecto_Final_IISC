import os

class Settings:
    BROKER_HOST=os.getenv("BROKER_HOST","localhost")
    PASSWORD=os.getenv("PASSWORD","mongo12345")
    DB_USER=os.getenv("DB_USER","usuario_mongo")
    DATABASE=os.getenv("DB","central")
    HOST=os.getenv("HOST","localhost")
    ENV = os.getenv("ENV", "local") 
    COMMAND = {"DATA": "data", "TOPIC": "topic", "QUERY": "query"}