from sqlalchemy import (
    Column, String, DECIMAL, Integer, BIGINT, TIMESTAMP, Enum, TEXT,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class PaymentStatus(enum.Enum):
    INTENDED = "INTENDED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"

class TransactionType(enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class AccountType(enum.Enum):
    USER_BALANCE = "USER_BALANCE"
    TUITION_DEBT = "TUITION_DEBT"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(CHAR(36), primary_key=True, index=True)  # UUID text
    payer_id = Column(String(10), nullable=False, index=True)
    student_id = Column(String(10), nullable=False, index=True)
    term = Column(String(32), nullable=False)
    amount = Column(DECIMAL(14, 2), nullable=False)
    payer_name = Column(String(255))
    payer_email = Column(String(100))
    payer_phone = Column(String(15))
    student_name = Column(String(255))
    idempotency_key = Column(String(64), unique=True)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.INTENDED)
    failure_reason = Column(TEXT)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # ---- relationships ----
    ledger_entries = relationship(
        "Ledger",
        back_populates="payment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    events = relationship(
        "PaymentEvent",
        back_populates="payment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    debt = relationship(   # 1:1
        "PaymentDebt",
        back_populates="payment",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Ledger(Base):
    __tablename__ = "ledger"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    payment_id = Column(
        CHAR(36),
        ForeignKey("payments.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    transaction_type = Column(Enum(TransactionType), nullable=False)
    account_ref = Column(String(64), nullable=False, index=True)
    amount = Column(DECIMAL(14, 2), nullable=False)
    balance_before = Column(DECIMAL(14, 2))
    balance_after = Column(DECIMAL(14, 2))
    description = Column(TEXT)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    payment = relationship("Payment", back_populates="ledger_entries")


class PaymentEvent(Base):
    __tablename__ = "payment_events"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    payment_id = Column(
        CHAR(36),
        ForeignKey("payments.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    event_type = Column(String(64), nullable=False)
    payload = Column(TEXT)
    user_ip = Column(String(45))
    user_agent = Column(TEXT)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    payment = relationship("Payment", back_populates="events")


class PaymentDebt(Base):
    __tablename__ = "payment_debts"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    payment_id = Column(
        CHAR(36),
        ForeignKey("payments.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,           # đảm bảo 1:1 ở mức DB
        index=True,
    )
    debt_id = Column(BIGINT)
    student_id = Column(String(10), nullable=False)
    term = Column(String(32), nullable=False)
    cleared_amount = Column(DECIMAL(14, 2), nullable=False)
    remaining_debt = Column(DECIMAL(14, 2))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    payment = relationship("Payment", back_populates="debt")
