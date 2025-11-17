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
    
    ALLOWLIST_PATHS: tuple[str, ...] = Field(..., env="ALLOWLIST_PATHS")
    # JWT phải trùng SECRET_KEY & ALGORITHM với auth service
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALG: str = Field(..., env="JWT_ALG")
    FRONTEND_URL: str = Field(..., env="FRONTEND_URL")

    # class Config:
    #     # env_file = ".env"
    #     env_file_encoding = "utf-8"
settings = Settings()
