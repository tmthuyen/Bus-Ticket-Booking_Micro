from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Union

# -------------------------
# ENUMS cho Pydantic
# -------------------------

class PaymentMethodEnum(str, Enum):
    VNPAY = "VNPAY"
    MOMO = "MOMO" 
    CASH = "CASH"

class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

# -------------------------
# REQUEST SCHEMAS
# -------------------------

class PaymentCreate(BaseModel):
    """Schema tạo payment mới"""
    booking_id: Union[str, UUID]  # Accept both string and UUID
    amount: Union[Decimal, int, float]  # Accept multiple number types
    method: PaymentMethodEnum
    description: Optional[str] = Field(None, max_length=255)
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Số tiền phải lớn hơn 0')
        return v

class MoMoPaymentMethodEnum(str, Enum):
    QR = "qr"              # QR Code scan
    WALLET = "wallet"       # MoMo wallet (SĐT + PIN)  
    CREDIT = "credit"       # Credit/Debit card
    ATM = "atm"            # ATM card
    INTERNET_BANKING = "internetbanking"  # Internet banking

class MoMoPaymentRequest(BaseModel):
    booking_id: Union[str, UUID]
    amount: Union[Decimal, int, float] = Field(..., gt=0)
    order_info: Optional[str] = Field("Thanh toán vé xe", max_length=255)
    customer_name: Optional[str] = Field(None, max_length=100)
    customer_phone: Optional[str] = Field(None, max_length=15)

    payment_method: Optional[MoMoPaymentMethodEnum] = Field(
        MoMoPaymentMethodEnum.CREDIT,
        description="Phương thức thanh toán MoMo"
    )

    redirect_url: Optional[str] = None
    ipn_url: Optional[str] = None



class MoMoCallbackRequest(BaseModel):
    """Schema callback từ MoMo"""
    partnerCode: str
    orderId: str
    requestId: str  
    amount: int
    orderInfo: str
    orderType: str
    transId: Optional[int] = None
    resultCode: int
    message: str
    payType: str
    responseTime: int
    extraData: Optional[str] = ""
    signature: str

class RefundRequest(BaseModel):
    """Schema yêu cầu hoàn tiền"""
    payment_id: UUID
    refund_amount: Optional[Decimal] = None  # None = hoàn toàn bộ
    reason: Optional[str] = Field(None, max_length=255)

# -------------------------
# RESPONSE SCHEMAS
# -------------------------

class PaymentOut(BaseModel):
    """Schema output payment"""
    id: UUID
    booking_id: UUID
    amount: Decimal
    method: str
    status: str
    description: Optional[str] = None
    provider_transaction_id: Optional[str] = None
    transaction_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2

class MoMoPaymentResponse(BaseModel):
    """Schema phản hồi tạo thanh toán MoMo"""
    payment_id: UUID
    order_id: str
    payment_url: Optional[str] = None
    qr_code_url: Optional[str] = None
    message: str
    success: bool

class PaymentStatusResponse(BaseModel):
    """Schema check status payment"""
    payment_id: UUID
    booking_id: UUID
    status: PaymentStatusEnum
    amount: Decimal
    method: PaymentMethodEnum
    transaction_time: datetime
    provider_transaction_id: Optional[str] = None
    message: str

class RefundResponse(BaseModel):
    """Schema phản hồi hoàn tiền"""
    payment_id: UUID
    refund_amount: Decimal
    status: str
    message: str
    refund_transaction_id: Optional[str] = None

# -------------------------
# LOG SCHEMAS
# -------------------------

class PaymentLogOut(BaseModel):
    """Schema output payment log"""
    id: UUID
    payment_id: UUID
    event_type: str
    event_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

# -------------------------
# COMMON SCHEMAS
# -------------------------

class APIResponse(BaseModel):
    """Schema response chung"""
    success: bool
    message: str
    data: Optional[Any] = None

class HealthCheck(BaseModel):
    """Schema health check"""
    service: str
    status: str
    timestamp: datetime
    version: str