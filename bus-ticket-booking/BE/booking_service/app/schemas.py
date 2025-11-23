from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from . import models

# Schema cho SeatAssignment
class SeatAssignmentBase(BaseModel):
    """Schema cơ bản cho phân công ghế"""
    seat_number: str = Field(..., min_length=1, max_length=10, description="Số ghế (A1, B2, ...)")

class SeatAssignmentResponse(SeatAssignmentBase):
    """Schema trả về thông tin phân công ghế"""
    id: str
    booking_id: str
    trip_id: int
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Schema cho Booking
class BookingCreate(BaseModel):
    """Schema tạo Booking mới (yêu cầu đặt vé)"""
    trip_id: int = Field(..., gt=0, description="ID chuyến xe")
    seat_numbers: List[str] = Field(..., min_length=1, description="Danh sách số ghế (A1, B2, ...)")
    
    # Thông tin khách hàng
    full_name: str = Field(..., min_length=1, max_length=100, description="Họ tên khách hàng")
    phone: str = Field(..., min_length=10, max_length=15, description="Số điện thoại")
    email: EmailStr = Field(..., description="Email khách hàng")
    
    total_price: float = Field(..., gt=0, description="Tổng giá vé")

class BookingUpdate(BaseModel):
    """Schema cập nhật Booking"""
    status: Optional[str] = Field(None, description="Trạng thái booking")

class BookingResponse(BaseModel):
    """Schema trả về thông tin Booking đầy đủ"""
    id: str
    trip_id: int
    booking_code: str
    full_name: str
    phone: str
    email: str
    status: str
    seat_quantity: int
    total_price: float
    created_at: datetime
    updated_at: datetime
    
    # Danh sách ghế đã đặt
    seat_assignments: Optional[List[SeatAssignmentResponse]] = None
    
    trip: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)

class BookingListResponse(BaseModel):
    """Schema trả về danh sách Booking (simplified)"""
    id: str
    booking_code: str
    trip_id: int
    full_name: str
    email: str
    seat_quantity: int
    total_price: float
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class BookingConfirmation(BaseModel):
    """Schema xác nhận đặt vé thành công"""
    booking_id: str
    booking_code: str
    message: str
    status: str

class BookedSeatsResponse(BaseModel):
    """Schema trả về danh sách ghế đã đặt theo chuyến xe"""
    trip_id: int
    booked_seat_numbers: List[str]
    total_booked: int 