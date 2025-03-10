from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.order import OrderStatusEnum

router = APIRouter()


@router.get("/", response_model=List[schemas.Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Kullanıcının siparişlerini listeler.
    """
    if crud.user.is_superuser(current_user) or crud.user.is_kitchen_staff(current_user):
        orders = crud.order.get_multi(db, skip=skip, limit=limit)
    else:
        orders = crud.order.get_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return orders


@router.post("/", response_model=schemas.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.OrderCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Yeni sipariş oluşturur.
    """
    order = crud.order.create_with_items(db=db, obj_in=order_in, user_id=current_user.id)
    return order


@router.get("/{id}", response_model=schemas.Order)
def read_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    ID'ye göre sipariş getirir.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    if not crud.user.is_superuser(current_user) and not crud.user.is_kitchen_staff(current_user) and (order.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Yeterli yetkiniz yok")
    return order


@router.put("/{id}/status", response_model=schemas.Order)
def update_order_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    status: OrderStatusEnum,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Sipariş durumunu günceller.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    order = crud.order.update_status(db=db, db_obj=order, status=status)
    return order


@router.put("/{id}", response_model=schemas.Order)
def update_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    order_in: schemas.OrderUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Siparişi günceller.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    if not crud.user.is_superuser(current_user) and not crud.user.is_kitchen_staff(current_user) and (order.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Yeterli yetkiniz yok")
    order = crud.order.update(db=db, db_obj=order, obj_in=order_in)
    return order 