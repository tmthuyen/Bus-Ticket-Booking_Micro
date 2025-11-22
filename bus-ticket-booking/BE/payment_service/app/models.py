from __future__ import annotations
from datetime import datetime
from typing import Optional, List
import enum
import uuid

from sqlalchemy import (
    String, DECIMAL, TIMESTAMP, TEXT, Enum, ForeignKey
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


# -------------------------
# PAYMENT MODEL
# -------------------------

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(
        CHAR(36),
        default=lambda: str(uuid4()),
        primary_key=True,
        index=True
    )

    booking_id: Mapped[str] = mapped_column(
        CHAR(36),
        unique=True,
        index=True,
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
        unique=True,
        index=True,
        nullable=True
    )

    payment_info: Mapped[Optional[str]] = mapped_column(
        TEXT,
        nullable=True
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    raw_response: Mapped[Optional[str]] = mapped_column(
        TEXT,
        nullable=True
    )

    secure_hash: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    # Relationship (1 Payment có nhiều PaymentLog)
    logs: Mapped[List["PaymentLog"]] = relationship(
        back_populates="payment",
        cascade="all, delete-orphan"
    )


# -------------------------
# PAYMENT LOG MODEL
# -------------------------

class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        index=True
    )

    payment_id: Mapped[str] = mapped_column(
        CHAR(36),
        ForeignKey("payments.id"),
        nullable=False
    )

    event_type: Mapped[str] = mapped_column(
        Enum("CREATED", "UPDATED", "FAILED", "EXPIRED",
             name="payment_event_type",
             native_enum=False),
        nullable=False
    )

    event_data: Mapped[Optional[str]] = mapped_column(
        TEXT,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.utcnow
    )

    # back reference
    payment: Mapped[Payment] = relationship(
        back_populates="logs"
    )
