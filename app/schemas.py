from pydantic import BaseModel, EmailStr
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
    is_admin: bool

class UrlAnalyticsView(BaseModel):
    id: UUID
    accessed_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    class Config:
        from_attributes = True

class HealthCheckResponse(BaseModel):
    status_code: int
    msg: str

class UserBase(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

class UserForm(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True
    is_admin: bool = False

class OAuth2PasswordRequestForm(BaseModel):
    username: str
    password: str

class OAuth2BaseResponse(BaseModel):
    token_type: str
    access_token: str
    expire_time: int 

class TokenData(BaseModel):
    current_active_uuid: UUID | None = None
    current_active_username: str | None = None