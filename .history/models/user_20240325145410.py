from pydantic import BaseModel
from pydantic import BaseModel, Field

class User(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    username: str  = Field(...)
    phone: str  = Field(...)

class UserInDB(User):
    id: int = Field(...)

    class Config:
        orm_mode = True
    
