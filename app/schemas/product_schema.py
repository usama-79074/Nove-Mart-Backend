from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Product create karte waqt ye data aayega
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    category_id: int


# Product update karte waqt - sab fields optional (partial update)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None


# Response mein ye data wapis jayega
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True
