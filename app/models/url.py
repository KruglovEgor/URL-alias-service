from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    clicks = Column(Integer, default=0)
    
    # Статистика переходов
    visits = relationship("URLVisit", back_populates="url", cascade="all, delete-orphan")


class URLVisit(Base):
    __tablename__ = "url_visits"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, nullable=False)
    visited_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    user_agent = Column(String)
    
    url = relationship("URL", back_populates="visits") 