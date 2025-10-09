from pymongo import MongoClient
from pymongo.collection import Collection
from .config import settings


class MongoDB:
    def __init__(self, uri: str = settings.MONGO_URI, db_name: str = settings.MONGO_DB):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]
    
    def get_collection(self, name: str) -> Collection:
        return self._db[name]
    

mongo = MongoDB()