from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.endpoints import url

app = FastAPI(title="URL Alias Service")

# Создаем таблицы при запуске
Base.metadata.create_all(bind=engine)

# Подключаем роутеры
app.include_router(url.router, tags=["urls"])

@app.get("/")
async def root():
    return {"message": "Welcome to URL Alias Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 