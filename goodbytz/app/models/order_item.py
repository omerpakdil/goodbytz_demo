from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrderItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menuitem.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    special_instructions = Column(String, nullable=True)
    
    # İlişkiler
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem") 