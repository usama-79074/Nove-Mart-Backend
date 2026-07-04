from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.order_schema import OrderResponse
from app.services import order_service
from app.utils.dependencies import get_current_user, get_current_admin
from app.models.user_model import User
from app.models.order_model import Order

router = APIRouter(prefix="/orders", tags=["Orders"])


# Cart se order create karna (checkout) - koi bhi logged-in user
@router.post("/create", response_model=OrderResponse)
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.create_order(db, current_user.id)


# Apne saare orders dekhna
@router.get("/", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_user_orders(db, current_user.id)


# Admin: store ke saare orders dekhna (kisi bhi customer ka ho)
# Note: ye route /{order_id} se pehle define hona zaroori hai,
# warna "all" ko order_id samajh liya jayega
@router.get("/all", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return db.query(Order).order_by(Order.created_at.desc()).all()


# Ek specific order ki detail dekhna (sirf apna order)
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_order_by_id(db, current_user.id, order_id)
