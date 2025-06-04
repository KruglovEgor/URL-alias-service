from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl


class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):
    pass


class URLVisitBase(BaseModel):
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class URLVisitCreate(URLVisitBase):
    url_id: int


class URLVisit(URLVisitBase):
    id: int
    visited_at: datetime
    url_id: int

    class Config:
        from_attributes = True


class URL(URLBase):
    id: int
    short_code: str
    is_active: bool
    created_at: datetime
    expires_at: datetime
    clicks: int
    visits: List[URLVisit] = []

    class Config:
        from_attributes = True


class URLList(BaseModel):
    total: int
    items: List[URL]


class URLStats(BaseModel):
    url_id: int
    original_url: str
    short_code: str
    total_clicks: int
    unique_visitors: int
    last_visited: Optional[datetime] = None 