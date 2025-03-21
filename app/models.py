import uuid
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Url(Base):
    __tablename__ = "urls"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String, unique=True)
    short_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    accessed_count = Column(Integer, default=0)

    # Relationship to analytics
    analytics = relationship("UrlAnalytics", back_populates="url", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    password_hash = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())

class UrlAnalytics(Base):
    __tablename__ = "url_analytics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    short_code = Column(String, ForeignKey("urls.short_code"),  nullable=False)
    accessed_at = Column(DateTime, default=func.now())
    ip_address = Column(String)
    user_agent = Column(String)

    # Relationship to url
    url = relationship("Url", back_populates="analytics")