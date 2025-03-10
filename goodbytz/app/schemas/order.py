from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.order import OrderStatusEnum
from app.schemas.order_item import OrderItem, OrderItemCreate


# Ortak özellikler
class OrderBase(BaseModel):
    notes: Optional[str] = None
    table_number: Optional[int] = None
    is_takeaway: Optional[bool] = False


# Oluşturma sırasında kullanılacak özellikler
class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


# Güncelleme sırasında kullanılacak özellikler
class OrderUpdate(OrderBase):
    status: Optional[OrderStatusEnum] = None


# Veritabanından okuma sırasında kullanılacak özellikler
class OrderInDBBase(OrderBase):
    id: int
    user_id: int
    status: OrderStatusEnum
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# API'den döndürülecek sipariş
class Order(OrderInDBBase):
    items: List[OrderItem] = []


# Mutfak personeli için sipariş özeti
class KitchenOrderSummary(BaseModel):
    id: int
    status: OrderStatusEnum
    table_number: Optional[int] = None
    is_takeaway: bool
    created_at: datetime
    items_count: int
    total_amount: float
    notes: Optional[str] = None
    items: List[OrderItem]
    
    class Config:
        orm_mode = True 