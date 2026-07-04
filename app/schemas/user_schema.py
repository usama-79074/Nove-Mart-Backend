from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Jab user register karega, ye data frontend se aayega
# role field yahan nahi raka - user sirf naam, email, password dega
# role automatically "customer" set hogi (auth_service mein)
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


# Jab user login karega, ye data aayega
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Jab hum user ka data response mein bhejenge (password kabhi nahi bhejna)
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # ORM object ko Pydantic model mein convert karne ke liye


# Login successful hone par token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
