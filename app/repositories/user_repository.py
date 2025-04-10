from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.schemas import UserForm
from app.models import User
from app.config import get_pwd_context
from typing import Optional
from fastapi import HTTPException, status

class UserRepository:
    """Persistence layer for user"""

    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_form: UserForm) -> Optional[User]:
        hashed_password = self._hash_password(user_form.password)
        new_user = User(
            username = user_form.username,
            email = user_form.email,
            password_hash = hashed_password,
            is_admin = user_form.is_admin
        )
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists."
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        return new_user
    
    def update_user(self, user_form: UserForm) -> Optional[User]:
        user = self.db.query(User).filter_by(username=user_form.username).first()
        if not user:
            return None
        for key, value in user_form.model_dump(exclude_unset=True).items():
            if key == "password":
                setattr(user, "password_hash", self._hash_password(value))
            else:
                setattr(user, key, value)    
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, username: str) -> bool:
       user = self.db.query(User).filter_by(username=username).first()
       if not user:
           return False
       self.db.delete(user)
       self.db.commit()
       return True
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate the user with username and password"""
        user = self.db.query(User).filter(User.username == username).first()
        if user and self._verify_password(password, user.password_hash):
            return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            return user
        return None

    
    @staticmethod
    def _hash_password(original_password: str) -> str:
        return get_pwd_context().hash(original_password)
    
    @staticmethod
    def _verify_password(original_password: str, hashed_password: str) -> bool:
        return get_pwd_context().verify(original_password, hashed_password)