import random
import string
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.url import URL, URLVisit


def generate_short_code(length: int = settings.SHORT_URL_LENGTH) -> str:
    """Генерация случайного короткого кода для URL"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_url(db: Session, original_url: str) -> URL:
    """Создание нового короткого URL"""
    short_code = generate_short_code()
    expires_at = datetime.utcnow() + timedelta(days=settings.URL_EXPIRATION_DAYS)
    
    db_url = URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_short_code(db: Session, short_code: str) -> Optional[URL]:
    """Получение URL по короткому коду"""
    return db.query(URL).filter(URL.short_code == short_code).first()


def get_urls(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True
) -> List[URL]:
    """Получение списка URL с пагинацией"""
    query = db.query(URL)
    if active_only:
        query = query.filter(URL.is_active == True)
    return query.offset(skip).limit(limit).all()


def deactivate_url(db: Session, url_id: int) -> Optional[URL]:
    """Деактивация URL"""
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url


def record_visit(
    db: Session,
    url_id: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> URLVisit:
    """Запись информации о посещении URL"""
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if db_url:
        db_url.clicks += 1
        
    visit = URLVisit(
        url_id=url_id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


def get_url_stats(db: Session, url_id: int) -> dict:
    """Получение статистики по URL"""
    url = db.query(URL).filter(URL.id == url_id).first()
    if not url:
        return None
        
    visits = db.query(URLVisit).filter(URLVisit.url_id == url_id).all()
    unique_visitors = len(set(visit.ip_address for visit in visits if visit.ip_address))
    
    return {
        "url_id": url.id,
        "original_url": url.original_url,
        "short_code": url.short_code,
        "total_clicks": url.clicks,
        "unique_visitors": unique_visitors,
        "last_visited": max(visit.visited_at for visit in visits) if visits else None
    } 