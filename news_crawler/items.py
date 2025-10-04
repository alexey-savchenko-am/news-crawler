
from pydantic import BaseModel
from typing import List
from datetime import datetime

class NewsItem(BaseModel):
    source: str
    title: str
    url: str
    date: datetime
    tags: List[str]
    content: str