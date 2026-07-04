from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base


# Orders table - jab user checkout karta hai to ek order banta hai
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, completed, cancelled, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Ek order ke andar multiple order items hote hain
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


# Order Items table - order ke andar konse products kitni quantity aur kis price par bike
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    # price yahan isliye save kar rahe hain (product ki current price nahi le rahe)
    # kyun ke future mein agar product ki price change ho jaye, purane order ki price wahi rahni chahiye
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
