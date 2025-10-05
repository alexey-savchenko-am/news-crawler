from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NewsDTO(BaseModel):
    id: str = Field(..., alias="_id")
    source: str
    title: str
    url: str
    date: datetime
    tags: List[str]
    content: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        
class NewsResponse(BaseModel):
    count: int
    items: List[NewsDTO]