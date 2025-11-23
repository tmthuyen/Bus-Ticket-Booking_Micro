from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder 
from sqlalchemy.orm import Session 
from datetime import timedelta
from typing import Annotated 
import logging

from . import repository, models, schemas, utils, response, helpers_api
from .database import engine, get_db
from .config import settings  
from fastapi.middleware.cors import CORSMiddleware
from . import rabbitmq_producer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)
 

tags_metadata = [
    {
        "name": "bookings",
        "description": "Operations with bookings.",
    },
]
# Khởi tạo ứng dụng FastAPI với thông tin cơ bản
app = FastAPI(
    title="Booking Service",  # Tên service
    description="Service xử lý thông tin đặt chỗ",  # Mô tả
    version="2.0.0",  # Phiên bản
    docs_url="/bookings/docs",  # Swagger UI path
    redoc_url="/bookings/redoc",  # ReDoc path
    openapi_tags=tags_metadata,  # Thêm thẻ (tags) cho OpenAPI
)

app.add_middleware( # cau hinh CORS
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn (có thể thay đổi để chỉ cho phép một số nguồn cụ thể)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các tiêu đề
)


# RabbitMQ Producer instance
producer = None

@app.on_event("startup")
def startup_event():
    """Initialize RabbitMQ producer on startup"""
    global producer
    
    rabbitmq_config = {
        'host': settings.rabbitmq_host,
        'port': settings.rabbitmq_port,
        'username': settings.rabbitmq_user,
        'password': settings.rabbitmq_password
    }
    
    producer = rabbitmq_producer.get_producer(rabbitmq_config)
    
    if producer and producer.channel:
        logger.info("RabbitMQ Producer initialized successfully")
    else:
        logger.warning("RabbitMQ Producer failed to initialize - falling back to HTTP notifications")


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    global producer
    if producer:
        producer.close()
    logger.info("Booking Service shutdown complete")


@app.get("/health", tags=["bookings"])
def health_check():
    """Kiểm tra trạng thái hoạt động của dịch vụ đặt chỗ."""
    return {"status": "Booking Service is healthy"}

@app.post("/", tags=["bookings"], status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: schemas.BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Tạo yêu cầu đặt vé (giữ chỗ tạm thời)
    - Kiểm tra dữ liệu đầu vào
    - Kiểm tra các ghế còn trống
    - Tạo booking với trạng thái PENDING
    - Tạo seat_assignments cho từng ghế
    """
    # Validate dữ liệu
    is_valid, msg = utils.is_valid_booking_data(
        full_name=booking_data.full_name,
        phone=booking_data.phone,
        email=booking_data.email,
        trip_id=booking_data.trip_id,
        seat_numbers=booking_data.seat_numbers,
        total_price=booking_data.total_price
    )
    
    if not is_valid:
        return response.errorResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg=msg
        )
    
    # Kiểm tra các ghế còn trống
    all_available, unavailable_seats = repository.check_seats_available(
        db, 
        booking_data.trip_id, 
        booking_data.seat_numbers
    )
    
    if not all_available:
        return response.errorResponse(
            status_code=status.HTTP_409_CONFLICT,
            msg=f"Các ghế sau đã được đặt: {', '.join(unavailable_seats)}. Vui lòng chọn ghế khác"
        )
    
    # Tạo booking code
    booking_code = utils.generate_booking_code()
    
    # Tạo booking với seat_assignments
    db_booking = repository.create_booking(
        db,
        trip_id=booking_data.trip_id,
        seat_numbers=booking_data.seat_numbers,
        full_name=booking_data.full_name,
        phone=booking_data.phone,
        email=booking_data.email,
        total_price=booking_data.total_price,
        booking_code=booking_code
    )
    
    return response.successResponse(
        status_code=status.HTTP_201_CREATED,
        msg="Đặt vé thành công, vui lòng thanh toán trong 15 phút",
        data={
            "booking_id": db_booking.id,
            "booking_code": db_booking.booking_code,
            "status": db_booking.status.value,
            "seat_quantity": db_booking.seat_quantity,
            "seat_numbers": booking_data.seat_numbers,
            "total_price": float(db_booking.total_price)
        }
    )

@app.get("/", tags=["bookings"])
def get_all_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lấy danh sách tất cả bookings"""
    bookings = repository.get_all_bookings(db, skip=skip, limit=limit)
    
    bookings_data = []
    for booking in bookings:
        seat_numbers = [seat.seat_number for seat in booking.seat_assignments]
        bookings_data.append({
            "id": booking.id,
            "booking_code": booking.booking_code,
            "trip_id": booking.trip_id,
            "full_name": booking.full_name,
            "email": booking.email,
            "seat_quantity": booking.seat_quantity,
            "seat_numbers": seat_numbers,
            "total_price": float(booking.total_price),
            "status": booking.status.value,
            "created_at": booking.created_at.isoformat()
        })
    
    return response.successResponse(
        msg="Lấy danh sách booking thành công",
        data=bookings_data
    )

@app.get("/{booking_id}", tags=["bookings"])
def get_booking_by_id(
    booking_id: str,
    db: Session = Depends(get_db)
):
    """Lấy thông tin booking theo ID"""
    db_booking = repository.get_booking_by_id(db, booking_id)
    
    if not db_booking:
        return response.errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy booking"
        )
    
    booking_response = schemas.BookingResponse.model_validate(db_booking)
    
    return response.successResponse(
        msg="Lấy thông tin booking thành công",
        data=booking_response.model_dump(mode='json')
    )

@app.get("/code/{booking_code}", tags=["bookings"])
def get_booking_by_code(
    booking_code: str,
    db: Session = Depends(get_db)
):
    """Lấy thông tin booking theo booking code (để tra cứu)"""
    db_booking = repository.get_booking_by_code(db, booking_code)
    
    if not db_booking:
        return response.errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy booking với mã này"
        )
    
    booking_response = schemas.BookingResponse.model_validate(db_booking)
    
    return response.successResponse(
        msg="Lấy thông tin booking thành công",
        data=booking_response.model_dump(mode='json')
    )

@app.put("/{booking_id}/confirm", tags=["bookings"])
def confirm_booking(
    booking_id: str,
    db: Session = Depends(get_db)
):
    """
    Xác nhận booking sau khi thanh toán thành công
    Chuyển trạng thái từ PENDING -> PAID
    """
    db_booking = repository.get_booking_by_id(db, booking_id)
    
    if not db_booking:
        return response.errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy booking"
        )
    
    if db_booking.status != models.BookingStatus.PENDING:
        return response.errorResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg=f"Không thể xác nhận booking với trạng thái {db_booking.status.value}"
        )
    
    # Xác nhận booking
    updated_booking = repository.confirm_booking(db, booking_id)
    
    # Gửi email xác nhận qua RabbitMQ
    global producer
    if producer and producer.channel:
        try:
            seat_numbers = [seat.seat_number for seat in updated_booking.seat_assignments]
            producer.publish_booking_confirmation(
                to_email=updated_booking.email,
                booking_code=updated_booking.booking_code,
                customer_name=updated_booking.full_name,
                trip_info=f"Trip ID: {updated_booking.trip_id}",
                seat_numbers=seat_numbers,
                total_price=float(updated_booking.total_price),
                booking_time=updated_booking.created_at.strftime("%d/%m/%Y %H:%M:%S")
            )
            logger.info(f"Published booking confirmation event for {updated_booking.booking_code}")
        except Exception as e:
            logger.error(f"Failed to publish booking confirmation: {e}")
    
    return response.successResponse(
        msg="Xác nhận booking thành công",
        data={
            "booking_id": updated_booking.id,
            "booking_code": updated_booking.booking_code,
            "status": updated_booking.status.value
        }
    )

@app.put("/{booking_id}/cancel", tags=["bookings"])
def cancel_booking(
    booking_id: str,
    db: Session = Depends(get_db)
):
    """
    Hủy booking theo chính sách. Chỉ hủy được khi trạng thái là PENDING hoặc PAID
    """
    db_booking = repository.get_booking_by_id(db, booking_id)
    
    if not db_booking:
        return response.errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy booking"
        )
    
    # Kiểm tra trạng thái có thể hủy
    if db_booking.status in [models.BookingStatus.CANCELLED, models.BookingStatus.REFUNDED]:
        return response.errorResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg=f"Booking đã ở trạng thái {db_booking.status.value}"
        )
    
    # Kiểm tra chính sách hủy vé (ví dụ: trước 24h)
    # Giả sử booking_time là thời gian chuyến đi (cần lấy từ Trip Service)
    # Tạm thời cho phép hủy
    
    # Hủy booking
    updated_booking = repository.cancel_booking(db, booking_id)
    
    # Gửi email hủy booking qua RabbitMQ
    global producer
    if producer and producer.channel:
        try:
            producer.publish_booking_cancellation(
                to_email=updated_booking.email,
                booking_code=updated_booking.booking_code,
                customer_name=updated_booking.full_name,
                cancellation_reason="Khách hàng yêu cầu hủy"
            )
            logger.info(f"Published booking cancellation event for {updated_booking.booking_code}")
        except Exception as e:
            logger.error(f"Failed to publish booking cancellation: {e}")
    
    return response.successResponse(
        msg="Hủy booking thành công",
        data={
            "booking_id": updated_booking.id,
            "booking_code": updated_booking.booking_code,
            "status": updated_booking.status.value
        }
    )

@app.put("/{booking_id}/refund", tags=["bookings"])
def refund_booking(
    booking_id: str,
    db: Session = Depends(get_db)
):
    """
    Hoàn tiền cho booking CANCELLED -> REFUNDED
    """
    db_booking = repository.get_booking_by_id(db, booking_id)
    
    if not db_booking:
        return response.errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy booking"
        )
    
    if db_booking.status != models.BookingStatus.CANCELLED:
        return response.errorResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg="Chỉ có thể hoàn tiền cho booking đã hủy"
        )
    
    # Hoàn tiền
    updated_booking = repository.refund_booking(db, booking_id)
    
    # Gửi email hoàn tiền qua RabbitMQ
    global producer
    if producer and producer.channel:
        try:
            producer.publish_booking_refund(
                to_email=updated_booking.email,
                booking_code=updated_booking.booking_code,
                customer_name=updated_booking.full_name,
                refund_amount=float(updated_booking.total_price)
            )
            logger.info(f"Published booking refund event for {updated_booking.booking_code}")
        except Exception as e:
            logger.error(f"Failed to publish booking refund: {e}")
    
    return response.successResponse(
        msg="Hoàn tiền thành công",
        data={
            "booking_id": updated_booking.id,
            "booking_code": updated_booking.booking_code,
            "status": updated_booking.status.value
        }
    )

@app.get("/trip/{trip_id}/booked-seats", tags=["bookings"])
def get_booked_seats_by_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách ghế đã được đặt (RESERVED hoặc BOOKED) theo trip_id
    """
    booked_seat_numbers = repository.get_booked_seats_by_trip(db, trip_id)
    
    return response.successResponse(
        msg="Lấy danh sách ghế đã đặt thành công",
        data={
            "trip_id": trip_id,
            "booked_seat_numbers": booked_seat_numbers,
            "total_booked": len(booked_seat_numbers)
        }
    )

@app.get("/customer/{customer_email}", tags=["bookings"])
def get_bookings_by_customer_email(
    customer_email: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lấy danh sách booking của customer theo email"""
    bookings = repository.get_bookings_by_email(db, customer_email, skip=skip, limit=limit)
    
    if not bookings:
        return response.successResponse(
            msg="Không tìm thấy booking nào",
            data=[]
        )
    
    bookings_data = []
    for booking in bookings:
        seat_numbers = [seat.seat_number for seat in booking.seat_assignments]
        bookings_data.append({
            "id": booking.id,
            "booking_code": booking.booking_code,
            "trip_id": booking.trip_id,
            "seat_quantity": booking.seat_quantity,
            "seat_numbers": seat_numbers,
            "total_price": float(booking.total_price),
            "status": booking.status.value,
            "created_at": booking.created_at.isoformat()
        })
    
    return response.successResponse(
        msg="Lấy danh sách booking thành công",
        data=bookings_data
    )
#Lấy danh sách booking theo email và booking code
@app.get("/search/{customer_email}/{booking_code}", tags=["bookings"])
async def search_booking_by_email_and_code(
    customer_email: str,
    booking_code: str,
    db: Session = Depends(get_db)
):
    """Tìm kiếm booking theo email và booking code"""
    db_booking = repository.get_bookings_by_email_and_code(db, customer_email, booking_code)
    
    if not db_booking:
        return response.errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy booking với thông tin cung cấp"
        )
    
    booking_response = schemas.BookingResponse.model_validate(db_booking)
    
    try:
        success, trip_data = await helpers_api.get_trip_by_id_of_trip_service(db_booking.trip_id)
        if not success:
            return response.errorResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                msg=trip_data.get("detail", "Error fetching trip information")
            )
        booking_response.trip = trip_data.get("data", {})
    except Exception as e:
        return response.errorResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg=str(e)
        )
    
    return response.successResponse(
        msg="Lấy thông tin booking thành công",
        data=booking_response.model_dump(mode='json')
    )