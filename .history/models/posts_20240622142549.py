from pydantic import BaseModel
from bson import ObjectId
from typing import List
from datetime import datetime


class Post(BaseModel):
	title: str
	content: str
	author_id: ObjectId
	categories_id: List[ObjectId]
	tags: List[ObjectId]
    
    
    