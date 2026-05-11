import enum
import datetime as dt
import uuid
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR
from .database import Base

# Enum cho trạng thái booking
class BookingStatus(enum.Enum):
    PENDING = "PENDING"           # Đang chờ thanh toán
    PAID = "PAID"                 # Đã thanh toán
    CANCELLED = "CANCELLED"       # Đã hủy
    REFUNDED = "REFUNDED"         # Đã hoàn tiền

# Enum cho trạng thái ghế
class SeatStatus(enum.Enum):
    RESERVED = "RESERVED"         # Giữ chỗ (chờ thanh toán)
    BOOKED = "BOOKED"             # Đã đặt (đã thanh toán)

# Bảng bookings: Lưu thông tin đặt vé
class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[str] = mapped_column(
        CHAR(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    trip_id: Mapped[int] = mapped_column(sa.Integer, nullable=False, index=True)
    booking_code: Mapped[str] = mapped_column(
        sa.String(20), 
        unique=True, 
        nullable=False,
        index=True
    )
    
    # Thông tin khách hàng
    full_name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(sa.String(15), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    
    status: Mapped[BookingStatus] = mapped_column(
        sa.Enum(BookingStatus, name="booking_status", native_enum=False),
        nullable=False,
        server_default=BookingStatus.PENDING.value,
    )
    seat_quantity: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(
        sa.DECIMAL(10, 2), 
        nullable=False
    )
    
    # Thời gian giữ chỗ tạm thời (1 tiếng từ lúc tạo booking)
    hold_until: Mapped[Optional[dt.datetime]] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
        comment="Thời gian hết hạn giữ chỗ tạm thời"
    )
    
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=dt.datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=dt.datetime.utcnow,
        onupdate=dt.datetime.utcnow,
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    
    # Relationship với seat_assignments
    seat_assignments: Mapped[list["SeatAssignment"]] = relationship(
        "SeatAssignment", 
        back_populates="booking",
        cascade="all, delete-orphan"
    )

# Bảng seat_assignments: Lưu thông tin phân công ghế
class SeatAssignment(Base):
    __tablename__ = "seat_assignments"
    
    id: Mapped[str] = mapped_column(
        CHAR(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    booking_id: Mapped[str] = mapped_column(
        CHAR(36),
        sa.ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    trip_id: Mapped[int] = mapped_column(sa.Integer, nullable=False, index=True)
    seat_number: Mapped[str] = mapped_column(sa.String(10), nullable=False)
    status: Mapped[SeatStatus] = mapped_column(
        sa.Enum(SeatStatus, name="seat_status", native_enum=False),
        nullable=False,
        server_default=SeatStatus.RESERVED.value,
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=dt.datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )
    
    # Relationship với booking
    booking: Mapped["Booking"] = relationship(
        "Booking", 
        back_populates="seat_assignments"
    )
