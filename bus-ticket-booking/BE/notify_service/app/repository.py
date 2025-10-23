from sqlalchemy import and_
from sqlalchemy.orm import Session
from . import models, schemas , utils
import datetime


OTP_TTL_MINUTES = 5
OTP_LENGTH = 6
MAX_RETRY = 10

def create_otp_no_collision_simple(
    db: Session,
    *,
    username: str,
    payment_id: str,
    purpose: str,
    email: str,
):
    now = utils.now_utc()
    exp = utils.get_expiry(now, OTP_TTL_MINUTES)

    # (tuỳ chọn) vô hiệu OTP cũ cùng giao dịch nếu muốn 1 OTP/transaction
    db.query(models.Notification).filter(
        models.Notification.username == username,
        models.Notification.payment_id == payment_id,
        models.Notification.purpose == purpose,
        models.Notification.status == "unused",
        models.Notification.expires_at > now,
    ).update({models.Notification.status: "used"})
    db.commit()

    # Sinh OTP, nếu đụng mã đang còn hiệu lực thì sinh lại
    for _ in range(MAX_RETRY):
        code = utils.generate_otp(OTP_LENGTH)

        dup = db.query(models.Notification.id).filter(
            and_(
                models.Notification.code == code,            # so trùng mã
                models.Notification.status == "unused",      # còn "active"
                models.Notification.expires_at > now,        # chưa hết hạn
            )
        ).first()

        if dup:
            continue  # đụng → sinh lại

        rec = models.Notification(
            username=username,
            payment_id=payment_id,
            purpose=purpose, 
            code=code,                 # ĐƠN GIẢN: lưu plain code (có thể đổi thành hash)
            created_at=now,
            expires_at=exp,
            status="unused",
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec, code  # trả code để gửi email

    # nếu quá nhiều lần vẫn đụng → tăng độ dài OTP
    raise RuntimeError("OTP collision — hãy tăng OTP_LENGTH lên 7-8 số")

# Check spam OTP
def check_otp_spam(db: Session, username: str, payment_id: str, minutes: int = 5) -> bool:
    minutes_ago = utils.now_utc() - datetime.timedelta(minutes=minutes)
    count = db.query(models.Notification).filter(
        models.Notification.username == username,
        models.Notification.payment_id == payment_id,
        models.Notification.created_at >= minutes_ago
    ).count()
    return count >= 5  # nếu trong 3 phút đã gửi 5 lần thì coi là spam

# Thuyên lấy dữ liệu thông báo
def get_all_notifications(db: Session, skip:int=0, limit:int=100):
    return db.query(models.Notification).order_by(models.Notification.created_at.desc()).offset(skip).limit(limit).all()

def create_notification(db: Session, notification: schemas.NotificationCreate):
    db_notification = models.Notification(
        user_id=notification.user_id,
        code=notification.code,
        expires_at=notification.expires_at,
        created_at=datetime.datetime.utcnow()
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notification(db: Session, notification_id: int):
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()



# lay otp theo username
def get_otp_by_username(db: Session, username: str, otp: str, payment_id: str):
    query = (
        db.query(models.Notification)
        .filter(
            models.Notification.username == username,
            models.Notification.code == otp,
            models.Notification.payment_id == payment_id
        )
        .order_by(models.Notification.created_at.desc())
    )
    return query.first()

# tao otp 
def create_otp(db: Session, otp: schemas.NotificationCreate):
    db_otp = models.Notification(
        username=otp.username,
        payment_id=otp.payment_id,
        purpose=otp.purpose,
        code=otp.code,
        expires_at=otp.expires_at,
        created_at=datetime.datetime.utcnow()
    )
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp