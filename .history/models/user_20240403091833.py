from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from models.PyObjectId import *


class UserInDB(BaseModel):
    phone: str = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    role: str = Field(...)
    createdAt: str = Field(...)
    full_Name: str = Field(...)
    gender: str = Field(...)
    address: str = Field(...)
    DriverLicenseID : str = Field(...)
    # educate: str = Field(...)
    # languages: str = Field(...)
    # sparkles: str = Field(...)
    # jobs: str = Field(...)
    birthdate: str = Field(...)
    # introduce: str = Field(...)
    avatar: List[object] = Field(...)
    imagesID: List[object] = Field(...)


class UserRegister(BaseModel):
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    phone: str = Field(...)

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
    imageDriverLicenseID: List[object] = Field(...)
    birthdate: str = Field(...)
    DriverLicenseID : str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserUpdateRequest(BaseModel):
    phone: str = None
    full_name: str = None
    address: str = None
    username: str = None
    gender: str = None
    avatar: List[object] = None
    imageDriverLicenseID: List[object] = None
    birthdate: str =    None
    DriverLicenseID : str = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
