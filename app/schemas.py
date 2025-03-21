from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from typing import Optional


class ShortenRequestBody(BaseModel):
    original_url: str
    strategy: str
    custom_code: Optional[str] = None


class UrlView(BaseModel):
    id: UUID
    original_url: str
    short_code: str
    created_at: datetime
    accessed_count: int

    class Config:
        from_attributes = True

class UserView(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserForm(BaseModel):
    username: str
    password: str
    email: str

class UrlAnalyticsView(BaseModel):
    id: UUID
    url_id: UUID 
    accessed_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    class Config:
        from_attributes = True

class HealthCheckResponse(BaseModel):
    status_code: int
    msg: str