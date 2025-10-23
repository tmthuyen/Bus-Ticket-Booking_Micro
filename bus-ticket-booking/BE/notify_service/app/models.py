import enum
from sqlalchemy import CHAR, Column, Integer, String, Text, Enum, DateTime
from datetime import datetime, timedelta, timezone
from .database import Base 

VIETNAM_TZ = timezone(timedelta(hours=7))



class PurposeType(enum.Enum):
    PAYMENT = "PAYMENT"
    LOGIN = "LOGIN"
    PASSWORD_RESET = "PASSWORD_RESET"
    
    
class Notification(Base):
    __tablename__ = 'otps'

    id = Column(Integer, primary_key=True, index=True) # khoi tao khoa chinh tu dong tang 
    username = Column(String(10),unique=False)  # ten dang nhap nguoi dung  
    payment_id = Column(CHAR(36), nullable=False) # ma giao dich lien ket voi OTP
    purpose = Column(Enum(PurposeType), nullable=True, default=PurposeType.PAYMENT) # muc dich thong bao
    code = Column(String(6), nullable=False) # ma thong bao (OTP)
    created_at = Column(DateTime, default=datetime.now(VIETNAM_TZ)) # thoi gian tao thong bao
    expires_at = Column(DateTime(timezone=True), nullable=False) # thoi gian het han thong bao
    used_at = Column(DateTime, nullable=True) # thoi gian su dung thong bao
    status = Column(Enum('unused', 'used', 'expired', name='status_enum'), default='unused') # trang thai thong bao: chua su dung, da su dung, het han
