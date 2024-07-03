from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]


class Post(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    content: str
    author_id: ObjectId
    categories_id: List[ObjectId]
    tags: List[ObjectId]
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
