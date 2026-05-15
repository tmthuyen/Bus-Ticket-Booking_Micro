import enum
import datetime as dt
import uuid
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR
from .database import Base

# Enum cho trạng thái OTP
class OTPStatus(enum.Enum):
    PENDING = "pending"      # Chờ sử dụng
    USED = "used"            # Đã sử dụng
    EXPIRED = "expired"      # Hết hạn

# Bảng otps: Lưu mã OTP để xác thực
class OTP(Base):
    __tablename__ = "otps"
    
    id: Mapped[str] = mapped_column(
        CHAR(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    email: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
        index=True
    )
    booking_code: Mapped[str] = mapped_column(
        sa.String(20),
        nullable=False,
        index=True,
        comment="Mã booking cần xác thực"
    )
    otp: Mapped[str] = mapped_column(
        sa.String(10),
        nullable=False
    )
    expiry_time: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False
    )
    status: Mapped[OTPStatus] = mapped_column(
        sa.Enum(OTPStatus, name="otp_status", native_enum=False),
        nullable=False,
        server_default=OTPStatus.PENDING.value,
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=dt.datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )
    attempts: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        server_default="0"
    )
