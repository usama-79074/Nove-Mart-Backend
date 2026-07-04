from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Category create karte waqt ye data aayega
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


# Category update karte waqt - dono fields optional rakhi hain
# taake user sirf jo field change karni hai wahi bheje
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Response mein ye data wapis jayega
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
