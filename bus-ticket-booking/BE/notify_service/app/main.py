import requests
from fastapi import BackgroundTasks, FastAPI, Depends
from fastapi.encoders import jsonable_encoder 
from . import models, schemas, repository, utils, repository, response
from .database import engine, SessionLocal
from sqlalchemy.orm import Session # thu vien sqlalchemy
# from datetime import datetime, timezone, time
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Optional

tags_metadata = [
    {
        "name": "notifications",
        "description": "Operations with notifications.",
    },
]
# Khởi tạo ứng dụng FastAPI với thông tin cơ bản
app = FastAPI(
    title="Notification Service",  # Tên service
    description="Service xử lý thông báo",  # Mô tả
    version="2.0.0",  # Phiên bản
    docs_url="/notifications/docs",  # Swagger UI path
    redoc_url="/notifications/redoc",  # ReDoc path
    openapi_tags=tags_metadata,  # Thêm thẻ (tags) cho OpenAPI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn (cẩn thận với việc này trong môi trường production)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các headers
)

models.Base.metadata.create_all(bind=engine) # tao tat ca cac bang trong database

# ham lay session db
def get_db(): # ham lay session db
    db = SessionLocal() # tao session db
    try:
        yield db # tra ve session db
    finally:
        db.close() # dong session db

@app.get("/health")
def read_root():
    return {"status": "ok", "message": "Welcome to the Notification Service API"}


# verify otp
@app.post("/verifyOTP", tags=["notifications"])
def verify_otp(request: schemas.VerifyOTPRequest, db: Session = Depends(get_db)):
    db_otp = repository.get_otp_by_username(db, request.username, request.code, request.payment_id)
    current_time = utils.get_current_time()

    if not db_otp:
        return response.errorResponse(status_code=404, msg="OTP không tồn tại")    

    # het han
    if db_otp.expires_at < current_time or db_otp.status == 'expired':
        db_otp.status = 'expired'
        db.commit()
        db.refresh(db_otp)
        return response.errorResponse(
            status_code=400,
            msg="OTP đã hết hạn",
        )

    # da su dung
    if db_otp.used_at is not None or db_otp.status == 'used':
        return response.errorResponse(
            status_code=400,
            msg="OTP đã được sử dụng",
        )

    # Cap nhat used_at neu OTP hop le
    db_otp.used_at = current_time
    db_otp.status = 'used'
    db.commit()
    db.refresh(db_otp)
    
    # utils.send_success_email(request.email)
    
    return response.successResponse(
                                        msg="Xác thực OTP thành công",
                                        data=jsonable_encoder({
                                            "valid": True,
                                            "message": "OTP hợp lệ và chưa được sử dụng"
                                        }),
                                    )

#generate otp
@app.post("/generateOTP/{username}", tags=["notifications"])
def generate_otp(request: schemas.GenerateOTPBody, background: BackgroundTasks, db: Session = Depends(get_db)): 
    is_spam = repository.check_otp_spam(db, request.username, request.payment_id, minutes=5)
    if is_spam:
        return response.errorResponse(status_code=429, msg="Gửi OTP quá nhiều lần, vui lòng thử lại sau")
    
    rec, code = repository.create_otp_no_collision_simple(
        db,
        username=request.username,
        payment_id=request.payment_id,
        purpose=request.purpose,
        email=request.email,
    ) 
    # gửi email ở background (tuỳ bạn)
    background.add_task(utils.send_otp_email, request.email, code)

    return response.successResponse(
                                        msg="Tạo OTP thành công",
                                        data=jsonable_encoder({
                                            "username": rec.username,
                                            "payment_id": rec.payment_id,
                                            "purpose": rec.purpose, 
                                            "expires_at": rec.expires_at,  # jsonable_encoder sẽ tự .isoformat()
                                        }),
                                    ) 
    #  set pending 
    # otp_code = utils.generate_otp()
    # current_time = utils.get_current_time()
    # expiry_time = utils.get_expiry(current_time, minutes=5)
    
    # # Luu otp_code va expiry_time vao database neu can thiet
    # otp_record = models.Notification(
    #     username=request.username,
    #     payment_id=request.payment_id,
    #     purpose=request.purpose,
    #     code=otp_code,
    #     created_at=current_time,
    #     expires_at=expiry_time,
    #     status='unused'  # set trang thai ban dau la 'unused'
    # )
 
    # utils.send_otp_email(request.email, otp_code)

    # db_otp = repository.create_otp(db, otp_record)
    # return response.successResponse(
    #                                     msg="Tạo OTP thành công",
    #                                     data=jsonable_encoder({
    #                                         "username": db_otp.username,
    #                                         "payment_id": db_otp.payment_id,
    #                                         "purpose": db_otp.purpose, 
    #                                         "expires_at": db_otp.expires_at,  # jsonable_encoder sẽ tự .isoformat()
    #                                     }),
    #                                 )

@app.post("/paymentNotification", tags=["notifications"])
def payment_notification(request: schemas.PaymentNotification, db: Session = Depends(get_db)):
    payment_email = utils.send_email_payment(request)
    return response.successResponse(msg="Tạo thông báo thanh toán thành công", data=jsonable_encoder(payment_email))
                                    
# Thuyên lấy dữ liệu thông báo
@app.get("/", tags=["notifications"])
def get_all_notifications(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    notifications = repository.get_all_notifications(db, skip=skip, limit=limit)
    return response.successResponse(msg="Lấy danh sách thông báo thành công",
                                     data=jsonable_encoder([schemas.NotificationDetail.model_validate(t).model_dump() for t in notifications])
                                        )
