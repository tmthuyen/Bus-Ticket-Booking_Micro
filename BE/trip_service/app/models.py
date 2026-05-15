# trip/models.py
import enum
import datetime as dt
from typing import List, Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .database import Base


# ===== Enums ===== 
class BaseStatus(enum.Enum):
    ACTIVE   = "ACTIVE"
    INACTIVE = "INACTIVE"
class BusStatus(enum.Enum):
    ACTIVE   = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"
class TripStatus(enum.Enum):
    SCHEDULED = "SCHEDULED"
    BOARDING  = "BOARDING"
    DEPARTED  = "DEPARTED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


# ===== Routes =====
class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    origin: Mapped[str] = mapped_column(sa.String(100), nullable=False, index=True)
    origin_code : Mapped[str | None] = mapped_column(sa.String(100), index=True)
    destination: Mapped[str] = mapped_column(sa.String(100), nullable=False, index=True)
    destination_code : Mapped[str | None] = mapped_column(sa.String(100), index=True)
    base_price: Mapped[float] = mapped_column(sa.Numeric(10, 2), nullable=False)
    distance_km: Mapped[float | None] = mapped_column(sa.Numeric(6, 1))
    estimated_duration: Mapped[int | None] = mapped_column(sa.Integer)  # minutes 
    status : Mapped[BaseStatus] = mapped_column(
        sa.Enum(BaseStatus, name="base_status", native_enum=False),
        nullable=False,
        server_default=BaseStatus.ACTIVE.value,
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # business uniqueness (cùng tuyến đi -> đến không trùng tên chữ hoa/thường)
    __table_args__ = (
        sa.UniqueConstraint("origin", "destination", name="uq_routes_origin_destination"),
        sa.UniqueConstraint("origin_code", "destination_code", name="uq_routes_origincode_destinationcode"),
    )

    trips: Mapped[List["Trip"]] = relationship(back_populates="route", cascade="all, delete-orphan")
    

# ===== Bus Model =====
class BusModel(Base):
    __tablename__ = "bus_models"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False, unique=True)
    total_seats: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    deck_count: Mapped[int] = mapped_column(sa.Integer, nullable=False, server_default="1")
    status: Mapped[BaseStatus] = mapped_column(
        sa.Enum(BaseStatus, name="base_status", native_enum=False),
        nullable=False,
        server_default=BaseStatus.ACTIVE.value,
    )   
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    
    buses: Mapped[List["Bus"]] = relationship(back_populates="bus_model", cascade="all, delete-orphan")
    seat_templates: Mapped[List["SeatTemplate"]] = relationship(back_populates="bus_model", cascade="all, delete-orphan")

# ===== Seat Template =====
class SeatTemplate(Base):
    __tablename__ = "seat_templates"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    bus_model_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("bus_models.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    seat_number: Mapped[str] = mapped_column(sa.String(10), nullable=False)  # e.g., A01, B12
    floor: Mapped[int | None] = mapped_column(sa.Integer)  # 1 or 2 for sleeper buses
    row_index: Mapped[int | None] = mapped_column(sa.Integer)  # từ 1 đến n
    col_index: Mapped[int | None] = mapped_column(sa.Integer)  # từ 1 đến n
    
    bus_model: Mapped["BusModel"] = relationship(back_populates="seat_templates")

    __table_args__ = (
        # mỗi số ghế là duy nhất trong 1 bus model
        sa.UniqueConstraint("bus_model_id", "seat_number", name="uq_seattemplates_busmodel_seatnumber"),
        sa.CheckConstraint("floor IS NULL OR floor IN (1, 2)", name="ck_seattemplates_floor_1_2"),
    )
    
# ===== Buses =====
class Bus(Base):
    __tablename__ = "buses"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    bus_model_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("bus_models.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    plate_number: Mapped[str] = mapped_column(sa.String(15), nullable=False, unique=True)
    status: Mapped[BusStatus] = mapped_column(
        sa.Enum(BusStatus, name="base_status", native_enum=False),
        nullable=False,
        server_default=BusStatus.ACTIVE.value,
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    
    trips: Mapped[List["Trip"]] = relationship(back_populates="bus", cascade="all, delete-orphan")
    bus_model: Mapped["BusModel"] = relationship(back_populates="buses")

# ===== Trips =====
class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    route_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("routes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    bus_id: Mapped[int | None] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("buses.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    departure_time: Mapped[dt.datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False, index=True)
    arrival_time: Mapped[dt.datetime | None] = mapped_column(sa.DateTime(timezone=True))
    total_seats: Mapped[int] = mapped_column(sa.Integer, nullable=False)

    status: Mapped[TripStatus] = mapped_column(
        sa.Enum(TripStatus, name="trip_status", native_enum=False),
        nullable=False,
        server_default=TripStatus.SCHEDULED.value,
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    route: Mapped["Route"] = relationship(back_populates="trips")
    bus: Mapped[Optional["Bus"]] = relationship(back_populates="trips")

    __table_args__ = (
        # đảm bảo available_seats không vượt quá tổng số ghế và không âm (Postgres CHECK) 
        sa.CheckConstraint("total_seats > 0", name="ck_trips_total_gt0"), 
    )

 