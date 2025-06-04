from fastapi import APIRouter

from app.api.v1.endpoints import urls, redirect

api_router = APIRouter()

# Подключаем эндпоинты
api_router.include_router(urls.router, prefix="/urls", tags=["urls"])
api_router.include_router(redirect.router, tags=["redirect"]) 