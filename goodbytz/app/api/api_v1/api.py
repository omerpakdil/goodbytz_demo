from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, menu_items, orders, kitchen

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(menu_items.router, prefix="/menu-items", tags=["menu-items"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(kitchen.router, prefix="/kitchen", tags=["kitchen"]) 