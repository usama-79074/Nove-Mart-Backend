from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token


# Naya user register karne ki logic
def register_user(db: Session, user_data: UserCreate):
    # Pehle check karo email already exist to nahi karta
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Password ko hash karke save karenge, plain text kabhi nahi
    # Role hamesha "customer" hogi - koi bhi user khud admin nahi ban sakta
    # Admin banana ho to seedha database mein update karna hoga
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="customer",  # default role hamesha customer hogi
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # database se generated id, created_at wapis le aana

    return new_user


# Login ki logic: email/password check karke JWT token banana
def login_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.email == login_data.email).first()

    # Agar user mila hi nahi, ya password galat hai
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Token ke andar user_id aur role daal rahe hain
    access_token = create_access_token(data={"user_id": user.id, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}
