from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.menu_item import CategoryEnum

router = APIRouter()


@router.get("/", response_model=List[schemas.MenuItem])
def read_menu_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[CategoryEnum] = Query(None, description="Kategori filtresi"),
    available_only: bool = Query(False, description="Sadece mevcut öğeleri göster"),
) -> Any:
    """
    Menü öğelerini listeler.
    """
    if category:
        menu_items = crud.menu_item.get_by_category(
            db, category=category, skip=skip, limit=limit
        )
    elif available_only:
        menu_items = crud.menu_item.get_available(db, skip=skip, limit=limit)
    else:
        menu_items = crud.menu_item.get_multi(db, skip=skip, limit=limit)
    return menu_items


@router.post("/", response_model=schemas.MenuItem)
def create_menu_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.MenuItemCreate,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Yeni menü öğesi oluşturur.
    """
    menu_item = crud.menu_item.get_by_name(db, name=item_in.name)
    if menu_item:
        raise HTTPException(
            status_code=400,
            detail="Bu isimde bir menü öğesi zaten var.",
        )
    menu_item = crud.menu_item.create(db, obj_in=item_in)
    return menu_item


@router.put("/{id}", response_model=schemas.MenuItem)
def update_menu_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.MenuItemUpdate,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Menü öğesini günceller.
    """
    menu_item = crud.menu_item.get(db, id=id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menü öğesi bulunamadı")
    menu_item = crud.menu_item.update(db, db_obj=menu_item, obj_in=item_in)
    return menu_item


@router.get("/{id}", response_model=schemas.MenuItem)
def read_menu_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    ID'ye göre menü öğesi getirir.
    """
    menu_item = crud.menu_item.get(db, id=id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menü öğesi bulunamadı")
    return menu_item


@router.delete("/{id}", response_model=schemas.MenuItem)
def delete_menu_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_kitchen_staff),
) -> Any:
    """
    Menü öğesini siler.
    """
    menu_item = crud.menu_item.get(db, id=id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menü öğesi bulunamadı")
    menu_item = crud.menu_item.remove(db, id=id)
    return menu_item 