from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import user as schemas
from app.services.user_service import UserService
from app.dependencies import get_db, get_user

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(user, db)

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return user_service.login_user(user, db)

@router.get("/me", response_model=schemas.UserResponse)
def me(user=Depends(get_user)):
    return user
