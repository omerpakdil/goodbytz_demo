from sqlalchemy import Boolean, Column, String, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.base_class import Base


class OrderStatusEnum(enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    READY = "Ready"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False)
    total_amount = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
    table_number = Column(Integer, nullable=True)
    is_takeaway = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan") 