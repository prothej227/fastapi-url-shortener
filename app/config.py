from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from passlib.context import CryptContext

class Settings(BaseSettings):
    app_name: str = "URL Shortener"
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()

@lru_cache
def get_pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")