from typing import Optional
from pydantic import BaseModel
from app.schemas.menu_item import MenuItem


# Ortak özellikler
class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int = 1
    special_instructions: Optional[str] = None
    unit_price: float


# Oluşturma sırasında kullanılacak özellikler
class OrderItemCreate(OrderItemBase):
    pass


# Güncelleme sırasında kullanılacak özellikler
class OrderItemUpdate(OrderItemBase):
    pass


# Veritabanından okuma sırasında kullanılacak özellikler
class OrderItemInDBBase(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True


# API'den döndürülecek sipariş öğesi
class OrderItem(OrderItemInDBBase):
    menu_item: Optional[MenuItem] = None 