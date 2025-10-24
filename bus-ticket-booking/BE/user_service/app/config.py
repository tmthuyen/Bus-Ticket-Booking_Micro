from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # db_host: str = Field(..., env="DB_HOST")
    # db_port: int = Field(..., env="DB_PORT")
    # db_user: str = Field(..., env="DB_USER")
    # db_pass: str = Field(..., env="DB_PASS")
    db_type: str = Field(..., env="DB_TYPE")
    db_name: str = Field(..., env="DB_NAME")
    db_root_url: str = Field(..., env="DB_ROOT_URL")
    app_port: int = Field(8000, env="APP_PORT")
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field(..., env="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(..., env="JWT_EXPIRE_MINUTES")
    
    @property
    def db_url(self) -> str:
        if self.db_type == "mysql":
            return f"{self.db_root_url}{self.db_name}"
        raise ValueError("Unsupported DB type")

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

import os
print("=== ENV ===")
for k, v in os.environ.items():
    if "JWT" in k:
        print(k, "=", v)

settings = Settings()

