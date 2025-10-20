from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import user as schemas
from app.services.user_service import UserService
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(user, db)

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return user_service.login_user(user, db)

@router.get("/me", response_model=schemas.UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user




from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["Users"])

class UserRegister(BaseModel):
    username: str
    email: str
    phone: str
    password: str
    age: int

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register_user(user: UserRegister):
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "role": "user"
    }

@router.post("/login")
def login_user(user: UserLogin):
    return {
        "access_token": "jwt.token.value",
        "token_type": "bearer"
    }

@router.get("/me")
def get_me():
    return {
        "id": 1,
        "username": "diyor",
        "email": "diyor@example.com",
        "role": "user"
    }
