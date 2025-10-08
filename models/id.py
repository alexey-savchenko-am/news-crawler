from pydantic import BaseModel, field_validator
from bson import ObjectId

class Id(ObjectId):
    pass 