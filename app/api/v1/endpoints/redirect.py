from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import url as url_service

router = APIRouter()


@router.get("/{short_code}")
def redirect_to_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Перенаправление на оригинальный URL"""
    db_url = url_service.get_url_by_short_code(db, short_code)
    
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL не найден"
        )
        
    if not db_url.is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="URL деактивирован"
        )
        
    if db_url.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="URL устарел"
        )
    
    # Записываем информацию о посещении
    url_service.record_visit(
        db,
        db_url.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return RedirectResponse(url=db_url.original_url) 