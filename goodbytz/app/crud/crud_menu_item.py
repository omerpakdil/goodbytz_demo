from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.menu_item import MenuItem, CategoryEnum
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate


class CRUDMenuItem(CRUDBase[MenuItem, MenuItemCreate, MenuItemUpdate]):
    def get_by_category(
        self, db: Session, *, category: CategoryEnum, skip: int = 0, limit: int = 100
    ) -> List[MenuItem]:
        return (
            db.query(self.model)
            .filter(MenuItem.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_available(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[MenuItem]:
        return (
            db.query(self.model)
            .filter(MenuItem.is_available == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[MenuItem]:
        return db.query(self.model).filter(MenuItem.name == name).first()


menu_item = CRUDMenuItem(MenuItem) 