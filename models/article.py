from pydantic import BaseModel, Field, field_validator
from bson import ObjectId
from typing import Optional, List
from datetime import datetime
from .id import Id

class Article(BaseModel):
    id: Optional[Id] = None
    source: str
    title: str
    url: str
    date: datetime
    tags: List[str]
    content: str

    model_config = {
        "arbitrary_types_allowed": True,
        "from_attributes": True
    }

    @field_validator("id", mode="before")
    @classmethod
    def convert_id(cls, v):
        if isinstance(v, ObjectId):
            return Id(v)
        return v