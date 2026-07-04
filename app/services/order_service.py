from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.cart_model import Cart, CartItem
from app.models.order_model import Order, OrderItem
from app.models.product_model import Product
from app.schemas.order_schema import OrderResponse, OrderItemResponse


# Cart se order create karna (checkout)
def create_order(db: Session, user_id: int):
    # User ka cart dhoondo
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart or len(cart.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty, cannot create order",
        )

    # Pehle saare items ka stock check kar lo (order banane se pehle)
    # taake agar koi ek bhi product out of stock ho to pura order fail ho, aadha na bane
    for cart_item in cart.items:
        product = cart_item.product
        if product.stock_quantity < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product: {product.name}",
            )

    # Total amount calculate karo
    total_amount = sum(item.product.price * item.quantity for item in cart.items)

    # Naya order banao
    new_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending",
    )
    db.add(new_order)
    db.flush()  # flush karne se new_order.id mil jata hai bina commit ke

    # Cart ke har item ko order item mein convert karo, aur stock kam karo
    for cart_item in cart.items:
        product = cart_item.product

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            price=product.price,  # us waqt ki price save kar rahe hain
        )
        db.add(order_item)

        # Stock mein se quantity minus karo
        product.stock_quantity -= cart_item.quantity

    # Order ban jane ke baad cart khali kar do
    for cart_item in cart.items:
        db.delete(cart_item)

    db.commit()
    db.refresh(new_order)

    return _build_order_response(new_order)


# Helper: Order model ko OrderResponse mein convert karta hai (product_name, subtotal ke sath)
def _build_order_response(order: Order):
    items_response = []
    for item in order.items:
        items_response.append(
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.price * item.quantity,
            )
        )

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=order.status,
        created_at=order.created_at,
        items=items_response,
    )


# Logged-in user ke saare orders dikhana
def get_user_orders(db: Session, user_id: int):
    orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
    return [_build_order_response(order) for order in orders]


# Ek specific order dekhna (sirf apna order, kisi aur ka nahi)
def get_order_by_id(db: Session, user_id: int, order_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return _build_order_response(order)
