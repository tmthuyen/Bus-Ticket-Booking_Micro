from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import threading
import logging

from . import models, schemas, repository, utils, response
from .database import engine, get_db
from .config import settings
from . import rabbitmq_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "otp",
        "description": "OTP verification operations."
    },
    {
        "name": "email",
        "description": "Email notification operations."
    },
]

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Notification & OTP Service",
    description="Service xử lý OTP xác thực và gửi email thông báo",
    version="3.0.0",
    docs_url="/notifications/docs",
    redoc_url="/notifications/redoc",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RabbitMQ Consumer Thread
consumer_thread = None

@app.on_event("startup")
def startup_event():
    """Start RabbitMQ consumer in background thread"""
    global consumer_thread
    
    rabbitmq_config = {
        'host': settings.rabbitmq_host,
        'port': settings.rabbitmq_port,
        'username': settings.rabbitmq_user,
        'password': settings.rabbitmq_password
    }
    
    consumer = rabbitmq_consumer.setup_consumer(rabbitmq_config)
    
    if consumer:
        consumer_thread = threading.Thread(target=consumer.start_consuming, daemon=True)
        consumer_thread.start()
        logger.info("RabbitMQ Consumer started in background thread")
    else:
        logger.warning("RabbitMQ Consumer failed to start - running in HTTP-only mode")


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Notification Service...")


@app.get("/health", tags=["otp"])
def health_check():
    return {"status": "Notification & OTP Service is healthy"}

@app.post("/otp/send", tags=["otp"], status_code=status.HTTP_201_CREATED)
def send_otp(
    otp_request: schemas.OTPCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Gửi mã OTP 6 chữ số qua email để xác thực booking
    """
    # Kiểm tra OTP gần nhất (rate limiting - 60 giây)
    latest_otp = repository.get_latest_otp(db, otp_request.email)
    if latest_otp and latest_otp.status == models.OTPStatus.PENDING:
        time_diff = (utils.get_current_datetime() - latest_otp.created_at).total_seconds()
        if time_diff < 60:  # Chờ ít nhất 60 giây
            return response.errorResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                msg=f"Vui lòng đợi {60 - int(time_diff)} giây trước khi yêu cầu OTP mới"
            )
    
    # Tạo mã OTP 6 chữ số
    otp_code = utils.generate_otp_code(length=6)
    expiry_minutes = 5
    
    # Lưu OTP vào database
    db_otp = repository.create_otp(
        db=db,
        email=otp_request.email,
        booking_code=otp_request.booking_code,
        otp_code=otp_code,
        expiry_minutes=expiry_minutes
    )
    
    # Gửi OTP qua email ngay lập tức (synchronous)
    # OTP cần gửi nhanh để user nhận được ngay
    try:
        utils.send_otp_email(
            receiver_email=otp_request.email,
            otp_code=otp_code,
            booking_code=otp_request.booking_code,
            expiry_minutes=expiry_minutes
        )
        logger.info(f"OTP sent successfully to {otp_request.email} for booking {otp_request.booking_code}")
    except Exception as e:
        logger.error(f"Failed to send OTP email: {e}")
        # OTP đã lưu DB, có thể retry sau hoặc user request lại
    
    return response.successResponse(
        status_code=status.HTTP_201_CREATED,
        msg="Mã OTP đã được gửi đến email của bạn",
        data={
            "otp_id": db_otp.id,
            "email": db_otp.email,
            "booking_code": db_otp.booking_code,
            "expiry_time": db_otp.expiry_time.isoformat(),
            "expires_in_minutes": expiry_minutes
        }
    )

@app.post("/otp/verify", tags=["otp"])
def verify_otp(
    otp_verify: schemas.OTPVerify,
    db: Session = Depends(get_db)
):
    """
    Xác thực mã OTP
    """
    # Validate format OTP (6 chữ số)
    is_valid, error_msg = utils.validate_otp_format(otp_verify.otp)
    if not is_valid:
        return response.errorResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg=error_msg
        )
    
    # Expire các OTP cũ trước
    repository.expire_old_otps(db)
    
    # Tìm OTP hợp lệ
    db_otp = repository.get_valid_otp(db, otp_verify.email, otp_verify.otp)
    
    if not db_otp:
        # Kiểm tra xem có OTP nào cho email này không
        latest_otp = repository.get_latest_otp(db, otp_verify.email)
        
        if not latest_otp:
            return response.errorResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                msg="Không tìm thấy mã OTP. Vui lòng yêu cầu mã OTP mới"
            )
        
        # OTP sai hoặc hết hạn, tăng số lần thử
        if latest_otp.status == models.OTPStatus.PENDING:
            repository.increment_otp_attempts(db, latest_otp.id)
            
            # Kiểm tra số lần thử
            if latest_otp.attempts + 1 >= 5:
                repository.mark_otp_as_expired(db, latest_otp.id)
                return response.errorResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    msg="Bạn đã nhập sai OTP quá 5 lần. Vui lòng yêu cầu mã OTP mới"
                )
            
            return response.errorResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                msg=f"Mã OTP không đúng. Còn {4 - latest_otp.attempts} lần thử"
            )
        
        if latest_otp.status == models.OTPStatus.USED:
            return response.errorResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                msg="Mã OTP này đã được sử dụng"
            )
        
        if latest_otp.status == models.OTPStatus.EXPIRED:
            return response.errorResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                msg="Mã OTP đã hết hạn. Vui lòng yêu cầu mã OTP mới"
            )
    
    # OTP đúng, đánh dấu đã sử dụng
    repository.mark_otp_as_used(db, db_otp.id)
    
    return response.successResponse(
        msg="Xác thực OTP thành công",
        data={
            "otp_id": db_otp.id,
            "email": db_otp.email,
            "booking_code": db_otp.booking_code,
            "verified": True
        }
    )

@app.get("/otp/email/{email}", tags=["otp"])
def get_otps_by_email(
    email: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Lấy lịch sử OTP theo email"""
    otps = repository.get_otps_by_email(db, email, skip=skip, limit=limit)
    
    otps_data = []
    for otp in otps:
        otps_data.append({
            "id": otp.id,
            "email": otp.email,
            "booking_code": otp.booking_code,
            "status": otp.status.value,
            "attempts": otp.attempts,
            "expiry_time": otp.expiry_time.isoformat(),
            "created_at": otp.created_at.isoformat()
        })
    
    return response.successResponse(
        msg="Lấy lịch sử OTP thành công",
        data=otps_data
    )

@app.get("/otp/{otp_id}", tags=["otp"])
def get_otp_by_id(
    otp_id: str,
    db: Session = Depends(get_db)
):
    """Lấy thông tin OTP theo ID"""
    db_otp = repository.get_otp_by_id(db, otp_id)
    
    if not db_otp:
        return response.errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy OTP"
        )
    
    otp_response = schemas.OTPResponse.model_validate(db_otp)
    
    return response.successResponse(
        msg="Lấy thông tin OTP thành công",
        data=otp_response.model_dump(mode='json')
    )

# EMAIL NOTIFICATION ENDPOINTS

@app.post("/email/booking-confirmation", tags=["email"])
def send_booking_confirmation(
    confirmation_email: schemas.BookingConfirmationEmail,
    background_tasks: BackgroundTasks
):
    """Gửi email xác nhận đặt vé"""
    
    def send_confirmation_task():
        utils.send_booking_confirmation_email(
            receiver_email=confirmation_email.to_email,
            booking_code=confirmation_email.booking_code,
            customer_name=confirmation_email.customer_name,
            trip_info=confirmation_email.trip_info,
            seat_numbers=confirmation_email.seat_numbers,
            total_price=confirmation_email.total_price,
            booking_time=confirmation_email.booking_time
        )
    
    background_tasks.add_task(send_confirmation_task)
    
    return response.successResponse(
        status_code=status.HTTP_202_ACCEPTED,
        msg="Email xác nhận đặt vé đang được gửi",
        data={"booking_code": confirmation_email.booking_code}
    )

@app.post("/email/booking-cancellation", tags=["email"])
def send_booking_cancellation(
    cancellation_email: schemas.BookingCancellationEmail,
    background_tasks: BackgroundTasks
):
    """Gửi email thông báo hủy vé"""
    
    def send_cancellation_task():
        utils.send_booking_cancellation_email(
            receiver_email=cancellation_email.to_email,
            booking_code=cancellation_email.booking_code,
            customer_name=cancellation_email.customer_name,
            cancellation_reason=cancellation_email.cancellation_reason
        )
    
    background_tasks.add_task(send_cancellation_task)
    
    return response.successResponse(
        status_code=status.HTTP_202_ACCEPTED,
        msg="Email hủy vé đang được gửi",
        data={"booking_code": cancellation_email.booking_code}
    )

@app.post("/email/booking-refund", tags=["email"])
def send_booking_refund(
    refund_email: schemas.BookingRefundEmail,
    background_tasks: BackgroundTasks
):
    """Gửi email thông báo hoàn tiền"""
    
    def send_refund_task():
        utils.send_booking_refund_email(
            receiver_email=refund_email.to_email,
            booking_code=refund_email.booking_code,
            customer_name=refund_email.customer_name,
            refund_amount=refund_email.refund_amount
        )
    
    background_tasks.add_task(send_refund_task)
    
    return response.successResponse(
        status_code=status.HTTP_202_ACCEPTED,
        msg="Email hoàn tiền đang được gửi",
        data={"booking_code": refund_email.booking_code, "refund_amount": refund_email.refund_amount}
    )
