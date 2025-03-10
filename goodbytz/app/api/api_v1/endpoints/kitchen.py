from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.order import OrderStatusEnum

router = APIRouter()


@router.get("/orders", response_model=List[schemas.KitchenOrderSummary])
def read_kitchen_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Mutfak personeli için sipariş özetlerini listeler.
    """
    orders = crud.order.get_kitchen_summary(db, skip=skip, limit=limit)
    return orders


@router.get("/orders/pending", response_model=List[schemas.Order])
def read_pending_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Bekleyen siparişleri listeler.
    """
    orders = crud.order.get_by_status(
        db, status=OrderStatusEnum.PENDING, skip=skip, limit=limit
    )
    return orders


@router.get("/orders/preparing", response_model=List[schemas.Order])
def read_preparing_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Hazırlanmakta olan siparişleri listeler.
    """
    orders = crud.order.get_by_status(
        db, status=OrderStatusEnum.PREPARING, skip=skip, limit=limit
    )
    return orders


@router.get("/orders/ready", response_model=List[schemas.Order])
def read_ready_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Hazır siparişleri listeler.
    """
    orders = crud.order.get_by_status(
        db, status=OrderStatusEnum.READY, skip=skip, limit=limit
    )
    return orders


@router.put("/orders/{id}/confirm", response_model=schemas.Order)
def confirm_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Siparişi onaylar.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    if order.status != OrderStatusEnum.PENDING:
        raise HTTPException(status_code=400, detail="Sipariş zaten onaylanmış")
    order = crud.order.update_status(db=db, db_obj=order, status=OrderStatusEnum.CONFIRMED)
    return order


@router.put("/orders/{id}/prepare", response_model=schemas.Order)
def prepare_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Siparişi hazırlanıyor durumuna getirir.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    if order.status != OrderStatusEnum.CONFIRMED:
        raise HTTPException(status_code=400, detail="Sipariş onaylanmamış")
    order = crud.order.update_status(db=db, db_obj=order, status=OrderStatusEnum.PREPARING)
    return order


@router.put("/orders/{id}/ready", response_model=schemas.Order)
def ready_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Siparişi hazır durumuna getirir.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    if order.status != OrderStatusEnum.PREPARING:
        raise HTTPException(status_code=400, detail="Sipariş hazırlanmıyor")
    order = crud.order.update_status(db=db, db_obj=order, status=OrderStatusEnum.READY)
    return order


@router.put("/orders/{id}/deliver", response_model=schemas.Order)
def deliver_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Siparişi teslim edildi durumuna getirir.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    if order.status != OrderStatusEnum.READY:
        raise HTTPException(status_code=400, detail="Sipariş hazır değil")
    order = crud.order.update_status(db=db, db_obj=order, status=OrderStatusEnum.DELIVERED)
    return order 