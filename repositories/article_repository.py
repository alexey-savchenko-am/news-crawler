from datetime import datetime, timezone, timedelta
from pymongo.collection import Collection
from typing import List, Dict, Any, Optional
from db.mongo import mongo
from models.article import Article
from models.id import Id
from bson import ObjectId

class ArticleRepository:
    def __init__(self):
        self._collection: Collection = mongo.get_collection("articles")

    def get_list(
        self, 
        source: Optional[str] = None, 
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10
    ) -> List[Article]:
    
        query = {}

        if source:
            query["source"] = source
            
        if tags:
            query["tags"] = {"$in": tags}

        date_filter = {}
        if start_date:
            date_filter["$gte"] = start_date

        if end_date:
            date_filter["$lte"] = end_date

        if date_filter:
            query["date"] = date_filter

        cursor = self._collection.find(query).limit(limit)
        return [Article(**doc) for doc in cursor]

    def get_recent(self, days: int = 7) -> List[Article]:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        cursor = self._collection.find({"date": {"$gte": since}})
        return [Article(**doc) for doc in cursor]
    
    def get_by_id(self, id: Id) -> Article | None:
        doc = self._collection.find_one({"_id": ObjectId(str(id))})
        if doc:
            return Article(**doc)
        return None
    
