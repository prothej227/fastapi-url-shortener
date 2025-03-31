from fastapi import FastAPI
from app.routes import router
from app.auth import auth

app = FastAPI()
app.include_router(router)
app.include_router(auth)