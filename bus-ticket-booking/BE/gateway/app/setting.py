from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    APP_NAME: str = "mini-gateway"
    # map prefix -> backend base url (tên service trong docker-compose)
    ROUTES: Dict[str, str] = {
        "/users": "http://user_api:8000", 
        "/trips": "http://trip_api:8000",
        "/bookings": "http://booking_api:8000",
        "/payments": "http://payment_api:8000",
        "/notifications": "http://notification_api:8000",
    }
    # Các path KHÔNG cần JWT (login/đăng ký/health)
    ALLOWLIST_PATHS: tuple[str, ...] = (
        "/healthz",
        "/users/login",        # OAuth2 password flow của auth
        "/users",       # đăng ký user (POST)
    )
    # JWT phải trùng SECRET_KEY & ALGORITHM với auth service
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALG: str = Field(..., env="JWT_ALG")

    class Config:
        # env_file = ".env"
        env_file_encoding = "utf-8"
settings = Settings()
