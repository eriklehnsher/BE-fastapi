from pydantic import BaseModel
from bson import ObjectId
from typing import List
from datetime import datetime


class Post(BaseModel):
    id: ObjectId
    title: str
	content: str
	author_id: ObjectId
	categories_id: List[ObjectId]
	tags: List[ObjectId]
	created_at: datetime
	updated_at: datetime
    
    
    