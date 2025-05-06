from fastapi import FastAPI
from app.routes import router
from app.auth import auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", 
        "http://127.0.0.1:8080", 
        "http://localhost:3000",
        "https://mystify-dev.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],   # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],   # Allow all headers
)
app.include_router(router)
app.include_router(auth)
