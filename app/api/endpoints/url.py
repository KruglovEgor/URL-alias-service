from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.url import URL, URLCreate
from app.services.url import create_url, get_url_by_alias, increment_clicks

router = APIRouter()

@router.post("/urls/", response_model=URL)
def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    """Создает короткий URL"""
    return create_url(db=db, url=url)

@router.get("/urls/{alias}", response_model=URL)
def get_url(alias: str, db: Session = Depends(get_db)):
    """Получает информацию о URL по алиасу"""
    url = get_url_by_alias(db=db, alias=alias)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url

@router.get("/{alias}")
def redirect_to_url(alias: str, db: Session = Depends(get_db)):
    """Перенаправляет на оригинальный URL"""
    url = get_url_by_alias(db=db, alias=alias)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    url = increment_clicks(db=db, url=url)
    return {"url": url.original_url} 