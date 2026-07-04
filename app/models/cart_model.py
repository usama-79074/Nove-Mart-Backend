from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base


# Cart table - har user ka apna ek cart hota hai
class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Ek cart ke andar multiple items ho sakte hain
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


# Cart Items table - cart ke andar konse products kitni quantity mein hain
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)

    # Relationships - inse hum item.product aur item.cart directly access kar sakte hain
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
