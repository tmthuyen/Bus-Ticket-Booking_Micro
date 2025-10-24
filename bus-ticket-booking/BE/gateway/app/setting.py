from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Dict
import os

class Settings(BaseSettings):
    APP_NAME: str = "Gateway Bus Ticket Booking"
    # map prefix -> backend base url (tên service trong docker-compose)
    ROUTES: Dict[str, str] = Field(..., env="ROUTES")
    # ROUTES: Dict[str, str] = Field(..., env="ROUTES")
    print(ROUTES)
    print(Field(..., env="USER_SERVICE_URL"))
    # Các path KHÔNG cần JWT (login/đăng ký/health)
    # ALLOWLIST_PATHS: tuple[str, ...] = (
    #     "/healthz",
    #     "/users/login",        # OAuth2 password flow của auth
    #     "/users",       # đăng ký user (POST)
    # )
    ALLOWLIST_PATHS: tuple[str, ...] = Field(..., env="ALLOWLIST_PATHS")
    # JWT phải trùng SECRET_KEY & ALGORITHM với auth service
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALG: str = Field(..., env="JWT_ALG")

    # class Config:
    #     # env_file = ".env"
    #     env_file_encoding = "utf-8"
settings = Settings()
