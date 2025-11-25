from datetime import datetime, timezone, timedelta
from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from typing import List, Dict, Any, Optional, Iterator
from db.mongo import mongo
from models.article import Article
from models.article_ml import ArticleML
from models.id import Id
from bson import ObjectId
from .base_repository import BaseRepository

class ArticleMLRepository(BaseRepository[ArticleML]):
    
    _collection_name = "articles_ml"

    @property
    def _model(self):
        return ArticleML
    
    def get_batches(
        self,
        batch_size: int = 500,
        is_processed: bool = False,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Iterator[List[ArticleML]]:
        query = self._prepare_query(is_processed, tags, start_date, end_date)
        cursor = self._collection.find(query, no_cursor_timeout=True)

        batch = []

        try:
            for doc in cursor:
                batch.append(ArticleML(**doc))
                if(len(batch) >= batch_size):
                    yield batch
                    batch = []
            if batch:
                yield batch
        finally:
            cursor.close()
            
    @staticmethod
    def _prepare_query(
        is_processed: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
         
        query = {}

        if is_processed is not None:
            if is_processed:
                query["processed_at"] = {"$exists": True, "$ne": None}
            else:
                query["$or"] = [{"processed_at": {"$exists": False}}, {"processed_at": None}]
            
        if tags:
            query["tags"] = {"$in": tags}

        date_filter = {}
        if start_date:
            date_filter["$gte"] = start_date

        if end_date:
            date_filter["$lte"] = end_date

        if date_filter:
            query["created_at"] = date_filter

        return query
