from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from middleware.auth import authenticate_user, create_access_token_for_user
from db import create_user, get_user_by_email
from middleware.auth import get_password_hash
from models.user import UserInDB

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup")
async def signup(user: UserInDB):
    user_exists = get_user_by_email(user.email)
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = get_password_hash(user.password)
    user_id = create_user(user)
    return {"user_id": user_id}

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}
