from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.url import URL, URLCreate, URLList, URLStats
from app.services import url as url_service

router = APIRouter()


@router.post("/", response_model=URL)
def create_short_url(
    url_in: URLCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Создание короткого URL"""
    db_url = url_service.create_url(db, str(url_in.original_url))
    return db_url


@router.get("/", response_model=URLList)
def get_urls(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Получение списка URL"""
    urls = url_service.get_urls(db, skip=skip, limit=limit, active_only=active_only)
    total = len(urls)
    return {"total": total, "items": urls}


@router.delete("/{url_id}", response_model=URL)
def deactivate_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Деактивация URL"""
    db_url = url_service.deactivate_url(db, url_id)
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL не найден"
        )
    return db_url


@router.get("/stats/{url_id}", response_model=URLStats)
def get_url_stats(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Получение статистики по URL"""
    stats = url_service.get_url_stats(db, url_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL не найден"
        )
    return stats 