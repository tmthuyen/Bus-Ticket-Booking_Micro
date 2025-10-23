from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_name: str = Field(..., env="DB_NAME")
    db_type: str = Field(..., env="DB_TYPE")
    app_port: int = Field(..., env="APP_PORT")
    @property
    def db_url(self) -> str:
        if self.db_type == "mysql":
            return f"mysql+mysqlconnector://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        raise ValueError("Unsupported DB type")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

