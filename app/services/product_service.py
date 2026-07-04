from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product_model import Product
from app.models.category_model import Category
from app.schemas.product_schema import ProductCreate, ProductUpdate


# Helper: check karta hai ke category_id valid hai ya nahi
def _validate_category_exists(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category_id, category does not exist",
        )


# Naya product banana (sirf admin)
def create_product(db: Session, product_data: ProductCreate):
    # Pehle check karo category exist karti hai ya nahi
    _validate_category_exists(db, product_data.category_id)

    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock_quantity=product_data.stock_quantity,
        category_id=product_data.category_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Saare products ki list nikalna
# category_id diya ho to us category ke products filter ho jayenge (optional filter)
def get_all_products(db: Session, category_id: int = None):
    query = db.query(Product)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    return query.all()


# Ek specific product ID se nikalna
def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


# Product update karna (sirf admin)
def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = get_product_by_id(db, product_id)

    # Agar category_id change ki ja rahi hai to usko bhi validate karo
    if product_data.category_id is not None:
        _validate_category_exists(db, product_data.category_id)
        product.category_id = product_data.category_id

    # Sirf wahi fields update karo jo bheji gayi hain
    if product_data.name is not None:
        product.name = product_data.name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.stock_quantity is not None:
        product.stock_quantity = product_data.stock_quantity

    db.commit()
    db.refresh(product)
    return product


# Product delete karna (sirf admin)
def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
