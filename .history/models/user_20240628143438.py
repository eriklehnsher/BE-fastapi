from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, validator

from bson import ObjectId
from typing import Annotated
from pydantic.functional_validators import BeforeValidator


PyObjectId = Annotated[str, BeforeValidator(str)]


class UserInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    phone: str = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    role: str = Field(...)
    createdAt: str = Field(...)
    full_Name: str = Field(...)
    gender: str = Field(...)
    address: str = Field(...)
    birthdate: str = Field(...)
    avatar: List[object] = Field(...)
   


class UserRegister(BaseModel):
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)
    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class UserUpdate(BaseModel):
    phone: str = Field(...)
    full_Name: str = Field(...)
    address: str = Field(...)
    username: str = Field(...)
    gender: str = Field(...)
    avatar: List[object] = Field(...)
    # imageDriverLicenseID: List[object] = Field(...)
    birthdate: str = Field(...)


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserUpdateRequest(BaseModel):
    phone: str = None
    full_Name: str = None
    address: str = None
    username: str = None
    gender: str = None
    avatar: List[object] = None
    # imageDriverLicenseID: List[object] = None
    birthdate: str = None


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
