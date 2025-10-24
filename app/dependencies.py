from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models, database
from app.core.security import verify_password
from app.db.models import UserRoles


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_admin(current_user = Depends(get_current_user)):
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not allawed.")
    
    return current_user

def get_user(current_user = Depends(get_current_user)):
    if current_user.role != UserRoles.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not allawed.")
    
    return current_user
