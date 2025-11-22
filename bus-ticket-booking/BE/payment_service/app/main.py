from decimal import Decimal
from fastapi import FastAPI, Depends, HTTPException, Request  
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from . import repository, models, schemas, utils
from .database import SessionLocal, engine, Base, get_db
from .config import settings
from .response import successResponse, errorResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware




# Tạo các bảng trong database nếu chưa tồn tại
models.Base.metadata.create_all(bind=engine)
tags_metadata = [
    {
        "name": "payments",
        "description": "Operations with payments.",
    },
]
# Khởi tạo ứng dụng FastAPI với thông tin cơ bản
app = FastAPI(
    title="Payment Service",  # Tên service
    description="Service xử lý thanh toán đặt vé xe",  # Mô tả
    version="2.0.0",  # Phiên bản
    docs_url="/payments/docs",  # Swagger UI path
    redoc_url="/payments/redoc",  # ReDoc path
    openapi_tags=tags_metadata,  # Thêm thẻ (tags) cho OpenAPI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn (cẩn thận với việc này trong môi trường production)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các headers
)
@app.post("/payments", response_model=schemas.PaymentOut, tags=["payments"])
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """Tạo một payment mới"""
    db_payment = repository.create_payment(
        db,
        booking_id=payment.booking_id,
        amount=payment.amount,
        method=payment.method,
    )
    return db_payment
  
@app.get("/payments/{payment_id}", response_model=schemas.PaymentOut, tags=["payments"])
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    """Lấy thông tin payment theo ID"""
    db_payment = repository.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

Base.metadata.create_all(bind=engine)

