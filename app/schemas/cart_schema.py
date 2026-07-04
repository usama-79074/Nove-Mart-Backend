from pydantic import BaseModel
from typing import List


# Cart mein product add karte waqt ye data aayega
class CartAddRequest(BaseModel):
    product_id: int
    quantity: int = 1


# Cart item ke andar product ki info bhi dikhayenge (taake frontend ko alag se call na karna pade)
class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    subtotal: float  # price * quantity

    class Config:
        from_attributes = True


# Pure cart ka response - saare items aur total amount
class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]
    total_amount: float

    class Config:
        from_attributes = True
