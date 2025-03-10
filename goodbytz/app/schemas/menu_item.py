from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.menu_item import CategoryEnum


# Ortak özellikler
class MenuItemBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category: Optional[CategoryEnum] = None
    preparation_time: Optional[int] = None
    is_available: Optional[bool] = True
    is_vegetarian: Optional[bool] = False
    is_vegan: Optional[bool] = False
    is_gluten_free: Optional[bool] = False


# Oluşturma sırasında kullanılacak özellikler
class MenuItemCreate(MenuItemBase):
    name: str
    price: float
    category: CategoryEnum


# Güncelleme sırasında kullanılacak özellikler
class MenuItemUpdate(MenuItemBase):
    pass


# Veritabanından okuma sırasında kullanılacak özellikler
class MenuItemInDBBase(MenuItemBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# API'den döndürülecek menü öğesi
class MenuItem(MenuItemInDBBase):
    pass 