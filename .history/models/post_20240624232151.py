from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional, Annotated
import datetime
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class PostInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    content: str
    author_name: str
    categories_name: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    images: List[object] = Field(...)

    class Config:
        arbitrary_types_allowed = True

