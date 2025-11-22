from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from . import models, schemas, utils
import datetime
from typing import List


def get_booking_by_id(db: Session, booking_id: str) -> models.Booking:
    """Lấy booking theo ID với seat_assignments"""
    return db.query(models.Booking)\
        .options(joinedload(models.Booking.seat_assignments))\
        .filter(models.Booking.id == booking_id)\
        .first()

def get_booking_by_code(db: Session, booking_code: str) -> models.Booking:
    """Lấy booking theo booking_code với seat_assignments"""
    return db.query(models.Booking)\
        .options(joinedload(models.Booking.seat_assignments))\
        .filter(models.Booking.booking_code == booking_code)\
        .first()

def get_bookings_by_email(db: Session, email: str, skip: int = 0, limit: int = 100):
    """Lấy danh sách booking theo email"""
    return db.query(models.Booking)\
        .options(joinedload(models.Booking.seat_assignments))\
        .filter(models.Booking.email == email)\
        .order_by(models.Booking.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_bookings_by_email_and_code(db: Session, email: str, booking_code: str) -> models.Booking:
    """Lấy booking theo email và booking_code"""
    return db.query(models.Booking)\
        .options(joinedload(models.Booking.seat_assignments))\
        .filter(models.Booking.email == email, models.Booking.booking_code == booking_code)\
        .first()

def get_bookings_by_trip(db: Session, trip_id: int, skip: int = 0, limit: int = 100):
    """Lấy danh sách booking theo trip_id"""
    return db.query(models.Booking)\
        .options(joinedload(models.Booking.seat_assignments))\
        .filter(models.Booking.trip_id == trip_id)\
        .order_by(models.Booking.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_all_bookings(db: Session, skip: int = 0, limit: int = 100):
    """Lấy tất cả bookings"""
    return db.query(models.Booking)\
        .options(joinedload(models.Booking.seat_assignments))\
        .order_by(models.Booking.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_booking(
    db: Session, 
    trip_id: int,
    seat_numbers: List[str],
    full_name: str,
    phone: str,
    email: str,
    total_price: float,
    booking_code: str
) -> models.Booking:
    """
    Tạo booking mới với nhiều ghế (giữ chỗ tạm thời)
    Tạo booking và seat_assignments tương ứng
    """
    # Tạo booking
    db_booking = models.Booking(
        trip_id=trip_id,
        booking_code=booking_code,
        full_name=full_name,
        phone=phone,
        email=email,
        status=models.BookingStatus.PENDING,
        seat_quantity=len(seat_numbers),
        total_price=total_price,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    db.add(db_booking)
    db.flush()  # Lấy booking.id mà chưa commit
    
    # Tạo seat_assignments cho từng ghế
    for seat_number in seat_numbers:
        seat_assignment = models.SeatAssignment(
            booking_id=db_booking.id,
            trip_id=trip_id,
            seat_number=seat_number,
            status=models.SeatStatus.RESERVED,
            created_at=datetime.datetime.utcnow()
        )
        db.add(seat_assignment)
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking_status(
    db: Session, 
    booking_id: str, 
    booking_status: models.BookingStatus,
    seat_status: models.SeatStatus = None
) -> models.Booking:
    """
    Cập nhật trạng thái booking và seat_assignments
    Nếu PAID: seat_status = BOOKED
    Nếu CANCELLED/REFUNDED: xóa seat_assignments
    """
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return None
    
    # Cập nhật booking status
    db_booking.status = booking_status
    db_booking.updated_at = datetime.datetime.utcnow()
    
    # Cập nhật seat_assignments status
    if booking_status == models.BookingStatus.PAID and seat_status:
        for seat in db_booking.seat_assignments:
            seat.status = seat_status
    elif booking_status in [models.BookingStatus.CANCELLED, models.BookingStatus.REFUNDED]:
        # Xóa seat_assignments khi hủy/hoàn tiền để giải phóng ghế
        for seat in db_booking.seat_assignments:
            db.delete(seat)
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

def confirm_booking(db: Session, booking_id: str) -> models.Booking:
    """Xác nhận booking sau khi thanh toán thành công"""
    return update_booking_status(
        db, 
        booking_id, 
        models.BookingStatus.PAID,
        models.SeatStatus.BOOKED
    )

def cancel_booking(db: Session, booking_id: str) -> models.Booking:
    """Hủy booking và giải phóng ghế"""
    return update_booking_status(db, booking_id, models.BookingStatus.CANCELLED)

def refund_booking(db: Session, booking_id: str) -> models.Booking:
    """Hoàn tiền booking"""
    return update_booking_status(db, booking_id, models.BookingStatus.REFUNDED)


def get_booked_seats_by_trip(db: Session, trip_id: int) -> List[str]:
    """
    Lấy danh sách seat_number đã được đặt (RESERVED hoặc BOOKED) theo trip_id
    API quan trọng để Frontend biết ghế nào đã đặt
    """
    seat_assignments = db.query(models.SeatAssignment.seat_number)\
        .filter(
            and_(
                models.SeatAssignment.trip_id == trip_id,
                models.SeatAssignment.status.in_([
                    models.SeatStatus.RESERVED,
                    models.SeatStatus.BOOKED
                ])
            )
        )\
        .all()
    
    return [seat.seat_number for seat in seat_assignments]

def check_seats_available(db: Session, trip_id: int, seat_numbers: List[str]) -> tuple[bool, List[str]]:
    """
    Kiểm tra danh sách ghế có còn trống không
    Return: (all_available: bool, unavailable_seats: List[str])
    """
    booked_seats = db.query(models.SeatAssignment.seat_number)\
        .filter(
            and_(
                models.SeatAssignment.trip_id == trip_id,
                models.SeatAssignment.seat_number.in_(seat_numbers),
                models.SeatAssignment.status.in_([
                    models.SeatStatus.RESERVED,
                    models.SeatStatus.BOOKED
                ])
            )
        )\
        .all()
    
    unavailable_seats = [seat.seat_number for seat in booked_seats]
    all_available = len(unavailable_seats) == 0
    
    return all_available, unavailable_seats
