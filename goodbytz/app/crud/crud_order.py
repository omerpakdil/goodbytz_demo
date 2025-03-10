from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.order import Order, OrderStatusEnum
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.mqtt_service import mqtt_service


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def create_with_items(
        self, db: Session, *, obj_in: OrderCreate, user_id: int
    ) -> Order:
        # Toplam tutarı hesapla
        total_amount = 0
        for item in obj_in.items:
            total_amount += item.unit_price * item.quantity
        
        # Siparişi oluştur
        db_obj = Order(
            user_id=user_id,
            status=OrderStatusEnum.PENDING,
            total_amount=total_amount,
            notes=obj_in.notes,
            table_number=obj_in.table_number,
            is_takeaway=obj_in.is_takeaway,
        )
        db.add(db_obj)
        db.flush()
        
        # Sipariş öğelerini oluştur
        for item in obj_in.items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
            if not menu_item:
                raise ValueError(f"Menü öğesi bulunamadı: {item.menu_item_id}")
            db_item = OrderItem(
                order_id=db_obj.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                special_instructions=item.special_instructions,
            )
            db.add(db_item)
        
        db.commit()
        db.refresh(db_obj)

        # Yeni sipariş bildirimi gönder
        mqtt_service.publish_order_status(db_obj.id, "PENDING")
        
        return db_obj
    
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(self.model)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(
        self, db: Session, *, status: OrderStatusEnum, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(self.model)
            .filter(Order.status == status)
            .order_by(Order.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_status(
        self, db: Session, *, db_obj: Order, status: OrderStatusEnum
    ) -> Order:
        old_status = db_obj.status
        db_obj.status = status
        if status == OrderStatusEnum.DELIVERED:
            db_obj.completed_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Sipariş durumu değişikliği bildirimi gönder
        if old_status != status:
            mqtt_service.publish_order_status(db_obj.id, status.value)
            
            # Mutfak bildirimi gönder
            if status == OrderStatusEnum.PENDING:
                mqtt_service.publish_kitchen_notification("new_order", {
                    "order_id": db_obj.id,
                    "table_number": db_obj.table_number,
                    "is_takeaway": db_obj.is_takeaway
                })
            elif status == OrderStatusEnum.READY:
                mqtt_service.publish_kitchen_notification("order_ready", {
                    "order_id": db_obj.id,
                    "table_number": db_obj.table_number,
                    "is_takeaway": db_obj.is_takeaway
                })
        
        return db_obj
    
    def get_kitchen_summary(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        orders = (
            db.query(self.model)
            .filter(Order.status.in_([
                OrderStatusEnum.PENDING,
                OrderStatusEnum.CONFIRMED,
                OrderStatusEnum.PREPARING,
                OrderStatusEnum.READY
            ]))
            .order_by(Order.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        result = []
        for order in orders:
            items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
            result.append({
                "id": order.id,
                "status": order.status,
                "table_number": order.table_number,
                "is_takeaway": order.is_takeaway,
                "created_at": order.created_at,
                "items_count": len(items),
                "total_amount": order.total_amount,
                "notes": order.notes,
                "items": items
            })
        
        return result


order = CRUDOrder(Order) 