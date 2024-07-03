from pydantic import BaseModel
from bson import ObjectId
from typing import  List
from datetime import datetime



class Post(BaseModel):
	title: str
    
    