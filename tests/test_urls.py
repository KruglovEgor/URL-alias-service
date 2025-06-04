from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.services import url as url_service
from app.core.config import settings

client = TestClient(app)


def test_create_short_url(db: Session):
    """Тест создания короткого URL"""
    response = client.post(
        "/api/v1/urls/",
        json={"original_url": "https://example.com"},
        auth=("admin", "admin")
    )
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://example.com"
    assert data["is_active"] is True


def test_get_urls(db: Session):
    """Тест получения списка URL"""
    response = client.get(
        "/api/v1/urls/",
        auth=("admin", "admin")
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_deactivate_url(db: Session):
    """Тест деактивации URL"""
    # Сначала создаем URL
    url = url_service.create_url(db, "https://example.com")
    
    response = client.delete(
        f"/api/v1/urls/{url.id}",
        auth=("admin", "admin")
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False


def test_redirect_to_url(db: Session):
    """Тест перенаправления по короткому URL"""
    # Создаем URL
    url = url_service.create_url(db, "https://example.com")
    
    response = client.get(f"/{url.short_code}", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"


def test_expired_url(db: Session):
    """Тест устаревшего URL"""
    # Создаем URL с истекшим сроком действия
    url = url_service.create_url(db, "https://example.com")
    url.expires_at = datetime.utcnow() - timedelta(days=1)
    db.commit()
    
    response = client.get(f"/{url.short_code}")
    assert response.status_code == 410


def test_inactive_url(db: Session):
    """Тест неактивного URL"""
    # Создаем и деактивируем URL
    url = url_service.create_url(db, "https://example.com")
    url.is_active = False
    db.commit()
    
    response = client.get(f"/{url.short_code}")
    assert response.status_code == 410


def test_url_stats(db: Session):
    """Тест статистики URL"""
    # Создаем URL и добавляем несколько посещений
    url = url_service.create_url(db, "https://example.com")
    url_service.record_visit(db, url.id, "127.0.0.1", "test-agent")
    url_service.record_visit(db, url.id, "127.0.0.1", "test-agent")
    url_service.record_visit(db, url.id, "127.0.0.2", "test-agent")
    
    response = client.get(
        f"/api/v1/urls/stats/{url.id}",
        auth=("admin", "admin")
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_clicks"] == 3
    assert data["unique_visitors"] == 2 