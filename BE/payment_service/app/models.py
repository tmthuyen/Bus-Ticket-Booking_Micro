from __future__ import annotations
from datetime import datetime
from typing import Optional, List
import enum
from uuid import uuid4  # ✅ FIXED: Thêm import uuid4

from sqlalchemy import (
    String, DECIMAL, TIMESTAMP, TEXT, Enum, ForeignKey, Index
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import (
    relationship, Mapped, mapped_column, DeclarativeBase
)

# -------------------------
# Base model  
# -------------------------

class Base(DeclarativeBase):
    pass

# -------------------------
# ENUMS
# -------------------------

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success" 
    FAILED = "failed"

class PaymentMethod(enum.Enum):
    VNPAY = "VNPAY"
    MOMO = "MOMO"
    CASH = "CASH"

class PaymentEventType(enum.Enum):
    CREATED = "CREATED"
    REQUEST_TRANSACTION = "REQUEST_TRANSACTION"
    CALLBACK = "CALLBACK"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    REFUND = "REFUND"

# -------------------------
# PAYMENT MODEL
# -------------------------

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(
        CHAR(36),
        default=lambda: str(uuid4()),  # ✅ FIXED: uuid4 được import
        primary_key=True,
        index=True
    )

    booking_id: Mapped[str] = mapped_column(
        CHAR(36),
        unique=True,    # ✅ CHỈ GIỮ unique=True, bỏ index=True
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
    )

    method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method", native_enum=False),
        nullable=False
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status", native_enum=False),
        default=PaymentStatus.PENDING,
        nullable=False
    )

    transaction_time: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.utcnow
    )

    provider_transaction_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,    # ✅ CHỈ GIỮ unique=True, bỏ index=True  
        nullable=True
    )

    payment_info: Mapped[Optional[str]] = mapped_column(
        TEXT,
        nullable=True,
        comment="Thông tin bổ sung về giao dịch (JSON)"
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    raw_response: Mapped[Optional[str]] = mapped_column(
        TEXT,
        nullable=True,
        comment="Dữ liệu phản hồi từ hệ thống thanh toán"
    )

    secure_hash: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Mã bảo mật HMAC để xác minh giao dịch"
    )

    # ✅ ENHANCED: Thêm fields mới
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.utcnow
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationship
    logs: Mapped[List["PaymentLog"]] = relationship(
        back_populates="payment",
        cascade="all, delete-orphan"
    )
    def to_dict(self) -> dict:
        """Convert Payment object to JSON-serializable dictionary"""
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "amount": str(self.amount),  # Convert Decimal to string
            "method": self.method.value if self.method else None,  # Get enum value
            "status": self.status.value if self.status else None,  # Get enum value  
            "description": self.description,
            "provider_transaction_id": self.provider_transaction_id,
            "transaction_time": self.transaction_time.isoformat() if self.transaction_time else None,
            # Handle optional timestamp fields safely
            "created_at": self.created_at.isoformat() if hasattr(self, 'created_at') and self.created_at else None,
            "updated_at": self.updated_at.isoformat() if hasattr(self, 'updated_at') and self.updated_at else None
        }

    

    # ✅ ENHANCED: Thêm indexes
    __table_args__ = (
        Index('ix_payments_booking_id', 'booking_id'),
        Index('ix_payments_status', 'status'),
        Index('ix_payments_method', 'method'),
        Index('ix_payments_created_at', 'created_at'),
    )

# -------------------------
# PAYMENT LOG MODEL  
# -------------------------

class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id: Mapped[str] = mapped_column(
        CHAR(36),
        default=lambda: str(uuid4()),  # ✅ FIXED
        primary_key=True,
        index=True
    )

    payment_id: Mapped[str] = mapped_column(
        CHAR(36),
        ForeignKey("payments.id", ondelete="CASCADE", onupdate="CASCADE"),  # ✅ FIXED
        nullable=False
    )

    event_type: Mapped[PaymentEventType] = mapped_column(
        Enum(PaymentEventType, name="payment_event_type", native_enum=False),
        nullable=False
    )

    event_data: Mapped[Optional[str]] = mapped_column(
        TEXT,
        nullable=True,
        comment="Thông tin chi tiết sự kiện (JSON format)"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.utcnow
    )

    # Relationship
    payment: Mapped[Payment] = relationship(
        back_populates="logs",
        passive_deletes=True 
    )
    def to_dict(self) -> dict:
        """Convert PaymentLog object to JSON-serializable dictionary"""
        return {
            "id": self.id,
            "payment_id": self.payment_id,
            "event_type": self.event_type.value if self.event_type else None,
            "event_data": self.event_data,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    # ✅ ENHANCED: Thêm indexes
    __table_args__ = (
        Index('ix_payment_logs_payment_id', 'payment_id'),
        Index('ix_payment_logs_event_type', 'event_type'),
        Index('ix_payment_logs_created_at', 'created_at'),
    )
    