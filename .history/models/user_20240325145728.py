from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    username: str  = Field(...)
    phone: str  = Field(...)

class UserInDB(User):
    id: Optional[str] = None

    class Config:
        orm_mode = True
    
