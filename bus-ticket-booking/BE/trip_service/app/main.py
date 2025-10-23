
from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder 
from sqlalchemy.orm import Session 
from datetime import timedelta
from typing import Annotated 

from . import repository, models, schemas, utils, response
from .database import SessionLocal, engine
from .config import settings  
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
 

tags_metadata = [
    {
        "name": "trips",
        "description": "Operations with trips.",
    },
]
# Khởi tạo ứng dụng FastAPI với thông tin cơ bản
app = FastAPI(
    title="Trip Service",  # Tên service
    description="Service xử lý thông tin chuyến đi",  # Mô tả
    version="2.0.0",  # Phiên bản
    docs_url="/trips/docs",  # Swagger UI path
    redoc_url="/trips/redoc",  # ReDoc path
    openapi_tags=tags_metadata,  # Thêm thẻ (tags) cho OpenAPI
)

app.add_middleware( # cau hinh CORS
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn (có thể thay đổi để chỉ cho phép một số nguồn cụ thể)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các tiêu đề
)

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()



# API endpoints sẽ được định nghĩa ở đây
@app.get("/health", tags=["trips"])
def health_check():
    """Kiểm tra trạng thái hoạt động của dịch vụ chuyến đi."""
    return {"status": "Trip Service is healthy"}