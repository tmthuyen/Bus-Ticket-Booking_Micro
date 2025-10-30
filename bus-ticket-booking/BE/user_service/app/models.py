import enum
import datetime as dt
from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .database import Base

class UserStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    PAYING = "PAYING"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"

class UserRole(enum.Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"
    # nếu MySQL + utf8mb4 + index unique => cân nhắc 191 thay vì 40
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(sa.String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(sa.String(11), nullable=True, unique=True)

    status: Mapped[UserStatus] = mapped_column(
        sa.Enum(UserStatus, name="user_status", native_enum=False),
        nullable=False,
        server_default=UserStatus.ACTIVE.value,        # default ở DB
    )
    role: Mapped[UserRole] = mapped_column(
        sa.Enum(UserRole, name="user_role", native_enum=False),
        nullable=False,
        server_default=UserRole.CUSTOMER.value,
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=dt.datetime.utcnow,                    # callable (không ngoặc)
        server_default=func.now(),                     # DB tự set
        nullable=False,
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=dt.datetime.utcnow,
        onupdate=dt.datetime.utcnow,                   # callable
        server_default=func.now(),
        # server_onupdate=func.now(),  # nếu muốn DB tự ON UPDATE CURRENT_TIMESTAMP (MySQL)
        nullable=False,
    )

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True, index=True)
    jti: Mapped[str] = mapped_column(sa.String(36), nullable=False, unique=True, index=True)
    token_hash: Mapped[str] = mapped_column(sa.String(255), nullable=False)  # sha256 hex=64

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("users.id", ondelete="CASCADE"),  # FK rõ ràng
        nullable=False,
        index=True,
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=dt.datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    ) 
    expires_at: Mapped[dt.datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[dt.datetime | None] = mapped_column(sa.DateTime(timezone=True))

    device_id: Mapped[str | None] = mapped_column(sa.String(255))
    ip: Mapped[str | None] = mapped_column(sa.String(45))
    user_agent: Mapped[str | None] = mapped_column(sa.String(255))
    rotated_to: Mapped[str | None] = mapped_column(sa.String(36))

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
