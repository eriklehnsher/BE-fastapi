from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional, Annotated
import datetime
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class TagInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str

    class Config:
        arbitrary_types_allowed = True

class TagModel(BaseModel):
    name: str

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Tag name"
            }
        }
        