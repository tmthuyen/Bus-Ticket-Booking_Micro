from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings): 
    # External Services
    user_service_url: str = Field(default="http://localhost:8003", env="USER_SERVICE_URL")
    trip_service_url: str = Field(default="http://localhost:8002", env="TRIP_SERVICE_URL")
    booking_service_url: str = Field(default="http://localhost:8003", env="BOOKING_SERVICE_URL")
    notify_service_url: str = Field(default="http://localhost:8005", env="NOTIFY_SERVICE_URL")

    #  db and app
    db_type: str = Field(..., env="DB_TYPE")
    db_name: str = Field(..., env="DB_NAME")
    db_root_url: str = Field(..., env="DB_ROOT_URL")
    app_port: int = Field(8000, env="APP_PORT")

    # MoMo URLs
    momo_partner_code: str = "MOMO"
    momo_access_key: str = "F8BBA842ECF85" 
    momo_secret_key: str = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    momo_endpoint: str = "https://test-payment.momo.vn/v2/gateway/api/create"
    momo_redirect_url: str = "http://localhost:8000/payments/momo/return"
    momo_ipn_url: str = "http://localhost:8000/payments/momo/callback" 
    
    @property
    def db_url(self) -> str:
        if self.db_type == "mysql":
            return f"{self.db_root_url}{self.db_name}"
        raise ValueError("Unsupported DB type")

    class Config:
        # env_file = ".env"
        env_file_encoding = "utf-8"


    service_name: str = "Payment Service"
    service_version: str = "1.0.0"

settings = Settings()