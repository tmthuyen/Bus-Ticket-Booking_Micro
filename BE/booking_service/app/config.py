from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings): 
    # External Services
    user_service_url: str = Field(..., env="USER_SERVICE_URL")
    trip_service_url: str = Field(..., env="TRIP_SERVICE_URL") 
    notify_service_url: str = Field(..., env="NOTIFY_SERVICE_URL")
    payment_service_url: str = Field(..., env="PAYMENT_SERVICE_URL")
    
    #  db and app
    db_type: str = Field(..., env="DB_TYPE")
    db_name: str = Field(..., env="DB_NAME")
    db_root_url: str = Field(..., env="DB_ROOT_URL")
    app_port: int = Field(8000, env="APP_PORT")
    
    # RabbitMQ
    rabbitmq_host: str = Field("rabbitmq", env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(5672, env="RABBITMQ_PORT")
    rabbitmq_user: str = Field("guest", env="RABBITMQ_USER")
    rabbitmq_password: str = Field("guest", env="RABBITMQ_PASSWORD")
    
    @property
    def db_url(self) -> str:
        if self.db_type == "mysql":
            return f"{self.db_root_url}{self.db_name}"
        raise ValueError("Unsupported DB type")

    class Config:
        # env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()