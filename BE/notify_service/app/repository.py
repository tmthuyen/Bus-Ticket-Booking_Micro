from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from . import models, schemas
import datetime


def create_otp(
    db: Session,
    email: str,
    booking_code: str,
    otp_code: str,
    expiry_minutes: int
) -> models.OTP:
    """Tạo OTP mới cho xác thực email"""
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes)
    
    db_otp = models.OTP(
        email=email,
        booking_code=booking_code,
        otp=otp_code,
        expiry_time=expiry_time,
        status=models.OTPStatus.PENDING,
        attempts=0,
        created_at=datetime.datetime.utcnow()
    )
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp

def get_otp_by_id(db: Session, otp_id: str) -> models.OTP:
    """Lấy OTP theo ID"""
    return db.query(models.OTP).filter(models.OTP.id == otp_id).first()

def get_valid_otp(db: Session, email: str, booking_code: str, otp_code: str) -> models.OTP:
    """
    Lấy OTP hợp lệ (pending, chưa hết hạn) theo email, booking_code và mã OTP
    """
    current_time = datetime.datetime.utcnow()
    return db.query(models.OTP)\
        .filter(
            and_(
                models.OTP.email == email,
                models.OTP.booking_code == booking_code,
                models.OTP.otp == otp_code,
                models.OTP.status == models.OTPStatus.PENDING,
                models.OTP.expiry_time > current_time
            )
        )\
        .order_by(models.OTP.created_at.desc())\
        .first()

def get_latest_otp(db: Session, email: str) -> models.OTP:
    """Lấy OTP mới nhất theo email"""
    return db.query(models.OTP)\
        .filter(models.OTP.email == email)\
        .order_by(models.OTP.created_at.desc())\
        .first()

def increment_otp_attempts(db: Session, otp_id: str) -> models.OTP:
    """Tăng số lần thử OTP sai"""
    db_otp = get_otp_by_id(db, otp_id)
    if not db_otp:
        return None
    
    db_otp.attempts += 1
    db.commit()
    db.refresh(db_otp)
    return db_otp

def mark_otp_as_used(db: Session, otp_id: str) -> models.OTP:
    """Đánh dấu OTP đã sử dụng"""
    db_otp = get_otp_by_id(db, otp_id)
    if not db_otp:
        return None
    
    db_otp.status = models.OTPStatus.USED
    db.commit()
    db.refresh(db_otp)
    return db_otp

def mark_otp_as_expired(db: Session, otp_id: str) -> models.OTP:
    """Đánh dấu OTP đã hết hạn"""
    db_otp = get_otp_by_id(db, otp_id)
    if not db_otp:
        return None
    
    db_otp.status = models.OTPStatus.EXPIRED
    db.commit()
    db.refresh(db_otp)
    return db_otp

def expire_old_otps(db: Session) -> int:
    """
    Đánh dấu tất cả OTP hết hạn (expiry_time < now và status = pending)
    Return: số lượng OTP đã expire
    """
    current_time = datetime.datetime.utcnow()
    expired_otps = db.query(models.OTP)\
        .filter(
            and_(
                models.OTP.status == models.OTPStatus.PENDING,
                models.OTP.expiry_time < current_time
            )
        )\
        .all()
    
    count = len(expired_otps)
    for otp in expired_otps:
        otp.status = models.OTPStatus.EXPIRED
    
    if count > 0:
        db.commit()
    
    return count

def get_otps_by_email(db: Session, email: str, skip: int = 0, limit: int = 50):
    """Lấy danh sách OTP theo email"""
    return db.query(models.OTP)\
        .filter(models.OTP.email == email)\
        .order_by(models.OTP.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_otps_by_booking_code(db: Session, booking_code: str):
    """Lấy danh sách OTP theo booking_code"""
    return db.query(models.OTP)\
        .filter(models.OTP.booking_code == booking_code)\
        .order_by(models.OTP.created_at.desc())\
        .all()