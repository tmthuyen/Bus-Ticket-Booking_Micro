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
    user_id = Column(String(36), nullable=False, index=True)
     