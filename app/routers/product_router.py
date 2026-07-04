from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service
from app.utils.dependencies import get_current_admin
from app.models.user_model import User

router = APIRouter(prefix="/products", tags=["Products"])


# Naya product banana - sirf admin
@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return product_service.create_product(db, product_data)


# Saare products dekhna - koi bhi (login zaroori nahi)
# ?category_id=1 query param se filter bhi kar sakte hain
@router.get("/", response_model=List[ProductResponse])
def get_products(
    category_id: Optional[int] = Query(None, description="Category ke hisab se filter karne ke liye"),
    db: Session = Depends(get_db),
):
    return product_service.get_all_products(db, category_id)


# Ek product ID se dekhna - koi bhi
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, product_id)


# Product update karna - sirf admin
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return product_service.update_product(db, product_id, product_data)


# Product delete karna - sirf admin
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return product_service.delete_product(db, product_id)
