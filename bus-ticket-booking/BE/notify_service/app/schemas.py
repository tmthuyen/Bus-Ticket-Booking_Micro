from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    username: str
    code: str
    expires_at: datetime
    used_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes  = True

class NotificationCreate(NotificationBase):
    pass

class NotificationDetail(NotificationBase):
    id: int
    payment_id: str
    purpose: str
    status: str
    class Config:
        from_attributes  = True

class Notification(NotificationBase):
    id: int
    class Config:
        from_attributes  = True

class GenerateOTPRequest(BaseModel):
    code : str
    expires_at : datetime
    class Config:
        from_attributes  = True

class VerifyOTPRequest(BaseModel):
    username: str
    payment_id: str
    code: str
    email: str
    class Config:
        from_attributes  = True

class VerifyOTPResponse(BaseModel):
    valid: bool
    message: str

class GenerateOTPBody(BaseModel):
    email: Optional[str]
    username: Optional[str]
    payment_id: Optional[str]
    purpose: Optional[str] = "PAYMENT"
    class Config:
        from_attributes  = True


class GenerateOTPResponse(BaseModel):
    username: str
    email: str

class PaymentNotification(BaseModel):
    subject: str = "Thanh toán học phí TDTU"
    payment_id: Optional[str] = None
    payer_id: Optional[str] = None
    payer_name: Optional[str] = None
    student_id: Optional[str] = None
    full_name: Optional[str] = None
    term: Optional[str] = None
    amount: Optional[float] = None
    payment_status: Optional[str] = None
    created_at: Optional[str] = None  # gửi ISO 8601
    updated_at: Optional[str] = None
    email: Optional[str] = None
    class Config:
        from_attributes  = True
    
