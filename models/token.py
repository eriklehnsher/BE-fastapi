from pydantic import BaseModel
from pydantic.fields import Field

class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)

    class Config:
        orm_mode = True