from sqlalchemy import Boolean, Column, String, Integer, Float, Text, DateTime, Enum
from sqlalchemy.sql import func
import enum

from app.db.base_class import Base


class CategoryEnum(str, enum.Enum):
    APPETIZER = "Appetizer"
    MAIN_COURSE = "Main Course"
    DESSERT = "Dessert"
    DRINK = "Drink"
    SIDE_DISH = "Side Dish"


class MenuItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    category = Column(Enum(CategoryEnum), nullable=False)
    preparation_time = Column(Integer, nullable=True)  # In minutes
    is_available = Column(Boolean(), default=True)
    is_vegetarian = Column(Boolean(), default=False)
    is_vegan = Column(Boolean(), default=False)
    is_gluten_free = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 