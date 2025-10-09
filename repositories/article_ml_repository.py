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