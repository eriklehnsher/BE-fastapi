from pydantic import BaseModel
from pydantic import BaseModel, Field

class Login(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

class UserInDB(BaseModel):
    id: int = Field(...)
    email: str  = Field(...)
    username: str  = Field(...)
    phone: str  = Field(...)
    password: str  = Field(...)

    class Config:
        orm_mode = True
    
