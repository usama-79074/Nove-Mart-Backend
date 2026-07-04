from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.cart_model import Cart, CartItem
from app.models.product_model import Product
from app.schemas.cart_schema import CartAddRequest, CartResponse, CartItemResponse


# Helper: user ka cart dhoondo, agar exist nahi karta to naya bana do
def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


# Cart mein product add karna
def add_to_cart(db: Session, user_id: int, item_data: CartAddRequest):
    # Pehle check karo product exist karta hai aur stock available hai
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if item_data.quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be at least 1",
        )

    if product.stock_quantity < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available",
        )

    # User ka cart nikalo (ya naya bana do)
    cart = get_or_create_cart(db, user_id)

    # Check karo ke ye product cart mein pehle se to nahi hai
    existing_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.product_id == item_data.product_id)
        .first()
    )

    if existing_item:
        # Agar pehle se hai to quantity badha do
        existing_item.quantity += item_data.quantity
    else:
        # Warna naya cart item bana do
        new_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
        )
        db.add(new_item)

    db.commit()
    return get_cart(db, user_id)


# User ka pura cart dikhana (items + total amount ke sath)
def get_cart(db: Session, user_id: int):
    cart = get_or_create_cart(db, user_id)

    items_response = []
    total_amount = 0.0

    # Har cart item ke sath product ki info bhi attach kar rahe hain
    for item in cart.items:
        subtotal = item.product.price * item.quantity
        total_amount += subtotal

        items_response.append(
            CartItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                subtotal=subtotal,
            )
        )

    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=items_response,
        total_amount=total_amount,
    )


# Cart se ek item remove karna
def remove_cart_item(db: Session, user_id: int, item_id: int):
    cart = get_or_create_cart(db, user_id)

    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart.id)
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )

    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}
