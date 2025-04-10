from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Url, UrlAnalytics, User
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID

class UrlRepository:
    """Repository for URL persistence layer"""

    def __init__(self, db: Session):
        self.db = db

    def save_short_url(self, original_url: str, short_code: str, user: User) -> bool:
        """Save the shortened URL"""
        new_url = Url(original_url=original_url, short_code=short_code, user=user)
        try:
            self.db.add(new_url)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return False
        return True
            
    def get_original_url(self, short_code: str) -> str:
        """Retrieve the original URL"""
        url_entry = self.db.query(Url).filter_by(short_code=short_code).first()
        return url_entry.original_url if url_entry else None

    def is_unique_short_code(self, short_code: str) -> bool:
        """Check if the short code is unique"""
        return self.db.query(Url).filter_by(short_code=short_code).first() is None

    def log_access(self, short_code: str, ip_address: str, user_agent: str):
        """Log analytics data"""
        analytics = UrlAnalytics(short_code=short_code, ip_address=ip_address, user_agent=user_agent)
        self.db.add(analytics)
        self.db.commit()

    def delete_short_url(self, short_code: str) -> bool:
        """Delete a short code"""
        url_entry = self.db.query(Url).filter_by(short_code=short_code).first()
        if url_entry:
            self.db.delete(url_entry)
            self.db.commit()
            return True
        return False
    
    def get_url_record(self, short_code: str) -> Url | None:
        """ Get URL record by short code """
        return self.db.query(Url).filter_by(short_code=short_code).first()
    
    def get_urls_by_user(self, user_uuid: UUID) -> Optional[List[Url]]:
        urls = self.db.query(Url).filter_by(user_uuid).all()
        return urls if urls else None
    
    def get_url_analytics(self, short_code: str) -> Optional[List[UrlAnalytics]]:
        return self.db.query(UrlAnalytics).filter_by(short_code=short_code).all()