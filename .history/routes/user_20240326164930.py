from socket import create_server
from fastapi import APIRouter, Body, Depends, status, HTTPException
from models.user import UserLogin, UserInDB, UserRegister
from fastapi.encoders import jsonable_encoder
from db import Users_db
from bson import ObjectId
from fastapi.responses import JSONResponse
from typing import List, Optional
from passlib.context import CryptContext
from models.token import *
import datetime
from jose import jwt
from config import settings
from middleware.auth import get_current_user


router = APIRouter()


def get_hashed_password(password: str):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


@router.post("/user/register", response_model=UserInDB)
async def create_user(user: UserRegister = Body(...)):
    email = user.model_dump()["email"]
    find_user_in_db =  Users_db.find_one({"email": email})
    if find_user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="email_already_used"
        )
    else:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = user.model_dump()
        user["password"] = get_hashed_password(user["password"])
        user["role"] = "customer"
        user["createdAt"] = now
        user["fullName"] = ""
        user["phone"] = ""
        user["address"] = ""
        user["educate"] = ""
        user["languages"] = ""
        user["sparkles"] = ""
        user["jobs"] = ""
        user["birthdate"] = ""
        user["introduce"] = ""
        new_user =  Users_db.insert_one(user)
        created_user = await Users_db.find_one({"_id": new_user.inserted_id})
        return created_user


def verify_password(password: str, hashed_password: str):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(
        password, hashed_password
    )


async def authenticate_user(email: str, password: str):
    user = await Users_db.find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


@router.post("/user/login", response_model=Token)
async def login(user_data: UserLogin = Body(...)):
    user_data = user_data.model_dump()
    user = await authenticate_user(user_data["email"], user_data["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=300)
    if user["role"] == "admin":
        access_token_expires = datetime.timedelta(minutes=600)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"], "name": user["username"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=List[UserInDB])
async def get_all_user(skip: int = 0, limit: int = 10):
    # Sử dụng skip và limit để phân trang nếu cần
    cursor = Users_db.find().skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    return users


@router.get("/user/email/{email}", response_model=UserInDB)
async def show_user(email: str):
    if (user := await Users_db.find_one({"email": email})) is not None:
        return user
    raise HTTPException(status_code=404, detail="user {email} not found")


@router.put("/user/update/{email}", response_model=UserInDB)
async def update_user(email: str, updated_user: UserInDB):
    updated_data = updated_user.model_dump(exclude_unset=True)

    # Các trường khác cần cập nhật
    updated_data = {
        "username":updated_data.get("username"),
        "email":updated_data.get("email"),
        "fullName": updated_data.get("fullName"),
        "phone": updated_data.get("phone"),
        "address": updated_data.get("address"),
        "educate": updated_data.get("educate"),
        "languages": updated_data.get("languages"),
        "sparkles": updated_data.get("sparkles"),
        "jobs": updated_data.get("jobs"),
        "birthdate": updated_data.get("birthdate"),
        "introduce": updated_data.get("introduce"),
    }

    result = await Users_db.update_one({"email": email}, {"$set": updated_data})

    if result.matched_count == 1 and result.modified_count == 1:
        updated_user = await Users_db.find_one({"email": email})
        return updated_user

    raise HTTPException(
        status_code=404, detail=f"User with email {email} not found or not updated"
    )