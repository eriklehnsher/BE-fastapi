from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional, Annotated
import datetime
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class PostInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str


    class Config:
        arbitrary_types_allowed = True
