from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime, timezone
from models.id import Id
from bson import ObjectId
from models.article import Article

class ArticleML(BaseModel):
    id: Optional[Id] = Field(default=None, alias="_id")
    article_id: Id
    content: str
    tags: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)),
    processed_at: Optional[datetime] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
        "from_attributes": True
    }

    @field_validator("id", "article_id", mode="before")
    @classmethod
    def convert_id(cls, v):
        if isinstance(v, ObjectId):
            return Id(v)
        return v