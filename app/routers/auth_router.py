from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, Token
from app.services import auth_service
from app.utils.dependencies import get_current_user, get_current_admin
from app.models.user_model import User

router = APIRouter(tags=["Authentication"])


# Naya user register karne ke liye
@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = auth_service.register_user(db, user_data)
    return new_user


# Login karke JWT token lene ke liye
@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    token = auth_service.login_user(db, login_data)
    return token


# Apni profile dekhne ke liye (login required, token bhejna zaroori hai)
@router.get("/profile", response_model=UserResponse)
def profile(current_user: User = Depends(get_current_user)):
    return current_user


# Admin: saare registered users ki list dekhna
@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return db.query(User).order_by(User.created_at.desc()).all()
