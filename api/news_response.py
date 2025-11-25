from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from models.article import Article


class NewsResponse(BaseModel):
    count: int
    items: List[Article]