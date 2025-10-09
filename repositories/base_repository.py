
from typing import Generic, TypeVar, Dict, Type, List, Any
from pydantic import BaseModel
from pymongo.collection import Collection
from db.mongo import mongo
from models.id import Id
from bson import ObjectId
from pymongo import UpdateOne
from pymongo.results import InsertOneResult, BulkWriteResult, InsertManyResult

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    
    _collection_name: str = ""

    def __init__(self):
        if not self._collection_name:
            raise ValueError("Collection name must be defined in subclass")
        self._collection: Collection = mongo.get_collection(self._collection_name)

    @property
    def _model(self) -> Type[T]:
        raise NotImplementedError
    
    def get_by_id(self, id: Id) -> T | None:
        doc = self._collection.find_one({"_id": id})
        if doc:
            return self._model(**doc)
        return None
    
    def create(self, item: T) -> Id:
        data = item.model_dump(by_alias=True, exclude_none=True)
        result = self._collection.insert_one(data)
        return Id(result.inserted_id)
    
    def create_many(self, items: List[T]) -> List[ObjectId]:
        if not items:
            return []
        
        data_list = [item.model_dump(by_alias=True, exclude_none=True) for item in items]
        result: InsertManyResult = self._collection.insert_many(data_list)
        return result.inserted_ids
    
    def update(self, id: Id, update_data: Dict[str, Any]) -> bool:
        result = self._collection.update_one(
            {"_id": id},
            {"$set": update_data}
        )

        return result.modified_count > 0
    
    def update_many(self, ids: List[Id], data: Dict[str, Any]) -> int:
        if not ids:
            return 0
        
        operations = [
            UpdateOne({"_id": _id}, {"$set": data})
            for _id in ids
        ]

        result: BulkWriteResult = self._collection.bulk_write(operations)
        return result.modified_count