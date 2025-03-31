from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from app.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from app.schemas import UserForm, UserBase
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from app.services.auth import create_access_token, get_settings, oauth2_scheme
from pydantic import BaseModel

class OAuth2PasswordRequestForm(BaseModel):
    username: str
    password: str

auth = APIRouter(prefix="/auth")

@auth.post(
    "/create", 
    response_model = UserBase,
    response_model_exclude_none=True,
    status_code = status.HTTP_201_CREATED
)
def create_user(request: UserForm, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.create_user(user_form=request)
    return user

@auth.post(
    "/update",
    response_model = UserBase,
    response_model_exclude_none=True,
    status_code = status.HTTP_200_OK
)
def update_user(request: UserForm, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.update_user(user_form = request)
    if not user is None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@auth.delete(
    "/delete",
    status_code=status.HTTP_200_OK
)
def delete_user(username: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    is_deleted = repo.delete_user(username)
    if is_deleted:
        return JSONResponse(content={"message": f"{username} has been deleted."})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username cannot be found.")

@auth.post(
    "/token",
    response_model=dict
)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.authenticate_user(username, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "expire_time": access_token_expires.total_seconds()}