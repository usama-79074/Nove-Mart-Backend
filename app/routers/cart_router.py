from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.cart_schema import CartAddRequest, CartResponse
from app.services import cart_service
from app.utils.dependencies import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/cart", tags=["Cart"])


# Cart mein product add karna - koi bhi logged-in user (customer ya admin)
@router.post("/add", response_model=CartResponse)
def add_to_cart(
    item_data: CartAddRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.add_to_cart(db, current_user.id, item_data)


# Apna pura cart dekhna
@router.get("/", response_model=CartResponse)
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.get_cart(db, current_user.id)


# Cart se ek item delete karna (item_id = cart_items table ka id)
@router.delete("/item/{item_id}")
def delete_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.remove_cart_item(db, current_user.id, item_id)
