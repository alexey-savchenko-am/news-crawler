from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from models.article import Article


class ArticleDTO(BaseModel):
    title: str
    url: str
    source: str
    date: datetime
    tags: List[str]
    content: str

    model_config = {
        "from_attributes": True
    }

class NewsResponse(BaseModel):
    count: int
    items: List[ArticleDTO]