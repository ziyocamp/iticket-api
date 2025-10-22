from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.db import models
from app.schemas import user as schemas
from app.core.security import get_password_hash, verify_password, create_access_token


class UserService:

    def register_user(self, user: schemas.UserCreate, db: Session) -> models.User:
        existing = db.query(models.User).filter(or_(
            models.User.username == user.username,
            models.User.phone == user.phone
        )).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username or Phone already exists")

        new_user = models.User(
            username=user.username,
            email=user.email,
            phone=user.phone,
            password=get_password_hash(user.password),
            age=user.age
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    def login_user(self, user: schemas.UserLogin, db: Session) -> schemas.Token:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username does not exists.")
        elif not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        token = create_access_token({"sub": db_user.username})

        return schemas.Token(access_token=token, token_type="bearer")
