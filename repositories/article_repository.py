from datetime import datetime, timezone, timedelta
from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from typing import List, Dict, Any, Optional, Iterator
from db.mongo import mongo
from models.article import Article
from models.id import Id
from bson import ObjectId
from .base_repository import BaseRepository

class ArticleRepository(BaseRepository[Article]):
    
    _collection_name = "articles"

    @property
    def _model(self):
        return Article

    def exists(self, url: str, title: str) -> bool:
        article = self._collection.find_one(
            {"$or": [{"url": url}, {"title": title}]},
            {"_id": 1}
        )
        return article is not None

    def get_list(
        self, 
        source: Optional[str] = None, 
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10
    ) -> List[Article]:
        query = self._prepare_query(source, tags, start_date, end_date)
        cursor = self._collection.find(query).limit(limit)
        return [Article(**doc) for doc in cursor]

    def get_recent(self, days: int = 7) -> List[Article]:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        cursor = self._collection.find({"date": {"$gte": since}})
        return [Article(**doc) for doc in cursor]
    
    def get_batches(
        self,
        batch_size: int = 500,
        is_processed: bool = False,
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Iterator[List[Article]]:
        
        """
        Return articles in batches of the specified size.
        Used for multithreaded processing or model training.
        """
        query = self._prepare_query(is_processed, source, tags, start_date, end_date)
        cursor = self._collection.find(query, no_cursor_timeout=True)

        batch = []
        try:
            for doc in cursor:
                batch.append(Article(**doc))
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch
        finally:
            cursor.close()

    @staticmethod
    def _prepare_query(
        is_processed: Optional[bool] = None,
        source: Optional[str] = None, 
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
            query["article_date"] = date_filter

        return query
