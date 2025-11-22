from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime
from . import models


class OTPCreate(BaseModel):
    """Schema tạo OTP mới"""
    user_id: Optional[str] = Field(None, description="ID người dùng (NULL nếu khách vãng lai)")
    email: EmailStr = Field(..., description="Email nhận OTP")
    type: str = Field(..., description="Loại OTP: booking, refund, update")
    booking_id: Optional[str] = Field(None, description="ID booking liên quan")

class OTPVerify(BaseModel):
    """Schema xác thực OTP"""
    email: EmailStr = Field(..., description="Email đã nhận OTP")
    otp: str = Field(..., min_length=6, max_length=8, description="Mã OTP cần xác thực")
    type: str = Field(..., description="Loại OTP: booking, refund, update")

class OTPResponse(BaseModel):
    """Schema trả về thông tin OTP"""
    id: str
    email: str
    expiry_time: datetime
    status: str
    type: str
    attempts: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class OTPSendResponse(BaseModel):
    """Schema response khi gửi OTP"""
    otp_id: str
    email: str
    expiry_time: datetime
    message: str

# EMAIL NOTIFICATION SCHEMAS 

class EmailNotificationRequest(BaseModel):
    """Schema yêu cầu gửi email thông báo tùy chỉnh"""
    to_email: EmailStr = Field(..., description="Email người nhận")
    subject: str = Field(..., description="Tiêu đề email")
    body: str = Field(..., description="Nội dung email")
    user_id: str = Field(..., description="ID người dùng")
    booking_id: str = Field(..., description="ID booking")

class NotificationResponse(BaseModel):
    """Schema trả về thông tin Notification (giữ để tương thích)"""
    id: str
    user_id: str
    booking_id: str
    type: str
    content: str
    sent_at: datetime
    status: str
    
    model_config = ConfigDict(from_attributes=True)

class BookingConfirmationEmail(BaseModel):
    """Schema gửi email xác nhận đặt vé"""
    to_email: EmailStr
    user_id: str
    booking_id: str
    booking_code: str
    customer_name: str
    trip_info: str
    seat_numbers: list[str]
    total_price: float
    booking_time: str

class BookingCancellationEmail(BaseModel):
    """Schema gửi email thông báo hủy vé"""
    to_email: EmailStr
    user_id: str
    booking_id: str
    booking_code: str
    customer_name: str
    cancellation_reason: Optional[str] = None

class BookingRefundEmail(BaseModel):
    """Schema gửi email thông báo hoàn tiền"""
    to_email: EmailStr
    user_id: str
    booking_id: str
    booking_code: str
    customer_name: str
    refund_amount: float

class NotificationListResponse(BaseModel):
    """Schema trả về danh sách thông báo"""
    id: str
    user_id: str
    booking_id: str
    type: str
    status: str
    sent_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
