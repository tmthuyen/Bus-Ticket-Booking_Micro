from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_name: str = Field(..., env="DB_NAME")
    db_type: str = Field(..., env="DB_TYPE")
    app_port: int = Field(8000, env="APP_PORT")
    
    # JWT Configuration
    # jwt_secret: str = Field(..., env="JWT_SECRET")
    # jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    # access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # External Services
    user_service_url: str = Field(..., env="USER_SERVICE_URL")
    trip_service_url: str = Field(..., env="TRIP_SERVICE_URL")
    booking_service_url: str = Field(..., env="BOOKING_SERVICE_URL")
    notify_service_url: str = Field(..., env="NOTIFY_SERVICE_URL")
    
    @property
    def db_url(self) -> str:
        if self.db_type == "mysql":
            return f"mysql+mysqlconnector://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        raise ValueError("Unsupported DB type")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()