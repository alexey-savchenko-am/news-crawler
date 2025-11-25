from pydantic import BaseModel, Field, field_validator, field_serializer
from bson import ObjectId
from typing import Optional, List
from datetime import datetime, timezone
from .id import Id

class Article(BaseModel):
    id: Optional[Id] = Field(default=None, alias="_id")
    source: str
    title: str
    url: str
    tags: List[str]
    content: str
    article_date: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: Optional[datetime] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "from_attributes": True
    }

    @field_serializer("id")
    def serialize_id(self, v, _info):
        return str(v) if v is not None else None

    @field_validator("id", mode="before")
    @classmethod
    def convert_id(cls, v):
        if isinstance(v, ObjectId):
            return Id(v)
        return v