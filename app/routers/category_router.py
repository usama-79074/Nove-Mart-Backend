from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services import category_service
from app.utils.dependencies import get_current_admin
from app.models.user_model import User

router = APIRouter(prefix="/categories", tags=["Categories"])


# Nayi category banana - sirf admin (get_current_admin dependency check karegi)
@router.post("/", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return category_service.create_category(db, category_data)


# Saari categories dekhna - koi bhi (login zaroori nahi)
@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db)


# Ek category ID se dekhna - koi bhi
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category_by_id(db, category_id)


# Category update karna - sirf admin
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return category_service.update_category(db, category_id, category_data)


# Category delete karna - sirf admin
@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return category_service.delete_category(db, category_id)
