from pydantic import BaseModel
from datetime import datetime
from typing import List


# Order ke andar ek item ka response
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: float          # us waqt ki price jis par bika tha
    subtotal: float        # price * quantity

    class Config:
        from_attributes = True


# Pura order response - items ke sath
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
