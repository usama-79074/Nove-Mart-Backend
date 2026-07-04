from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


# Nayi category banana (sirf admin)
def create_category(db: Session, category_data: CategoryCreate):
    # Pehle check karo ke same naam ki category already to nahi hai
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )

    new_category = Category(
        name=category_data.name,
        description=category_data.description,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# Saari categories ki list nikalna (koi bhi user dekh sakta hai)
def get_all_categories(db: Session):
    return db.query(Category).all()


# Ek specific category ID se nikalna
def get_category_by_id(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


# Category update karna (sirf admin)
def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
    category = get_category_by_id(db, category_id)  # agar na mili to 404 already raise ho jayega

    # Sirf wahi fields update karo jo user ne bheji hain (None wali skip)
    if category_data.name is not None:
        category.name = category_data.name
    if category_data.description is not None:
        category.description = category_data.description

    db.commit()
    db.refresh(category)
    return category


# Category delete karna (sirf admin)
def delete_category(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
