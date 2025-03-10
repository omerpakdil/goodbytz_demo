from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
import os
from sqlalchemy.orm import Session

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.services.mqtt_service import mqtt_service
from app.db.session import get_db
from app import crud, models

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Yemek Sipariş ve Yönetim Sistemi API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik dosyaları ve şablonları ekle
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# API rotalarını ekle
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/menu")
async def menu_page(request: Request, db: Session = Depends(get_db)):
    # Menü öğelerini veritabanından çek
    menu_items = crud.menu_item.get_available(db)
    return templates.TemplateResponse("menu.html", {"request": request, "menu_items": menu_items})

@app.get("/orders")
async def orders_page(request: Request):
    return templates.TemplateResponse("orders.html", {"request": request})

@app.get("/orders/{order_id}")
async def order_details_page(request: Request, order_id: int, db: Session = Depends(get_db)):
    # Siparişi veritabanından çek
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    
    # İlişkili verileri yükle
    db.refresh(order)
    for item in order.items:
        db.refresh(item)
        db.refresh(item.menu_item)
    
    return templates.TemplateResponse("order_details.html", {"request": request, "order": order})

@app.get("/kitchen")
async def kitchen_page(request: Request):
    return templates.TemplateResponse("kitchen.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Uygulama başladığında çalışacak işlemler."""
    logger.info("Uygulama başlatılıyor...")
    # MQTT servisini başlat
    mqtt_service.connect()
    logger.info("MQTT servisi başlatıldı")

@app.on_event("shutdown")
async def shutdown_event():
    """Uygulama kapanırken çalışacak işlemler."""
    logger.info("Uygulama kapatılıyor...")
    # MQTT servisini durdur
    mqtt_service.disconnect()
    logger.info("MQTT servisi durduruldu")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 