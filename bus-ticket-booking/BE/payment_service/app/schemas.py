# PAYMENT SCHEMAS - CÁC SCHEMA ĐỂ VALIDATION DỮ LIỆU

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum  

# ENUMS - CÁC GIÁ TRỊ ENUM

class PaymentStatus(str, Enum):
    """Trạng thái của payment trong quy trình thanh toán"""
    INTENDED = "INTENDED"     # Đã tạo ý định thanh toán, chờ xử lý
    PROCESSING = "PROCESSING" # Đang thực hiện giao dịch
    SUCCESS = "SUCCESS"       # Thanh toán thành công
    FAILED = "FAILED"         # Thanh toán thất bại
    EXPIRED = "EXPIRED"       # Hết hạn thanh toán

# PAYMENT SCHEMAS - CÁC SCHEMA CHO PAYMENT

class PaymentBase(BaseModel):
    """Schema cơ bản cho payment chứa các field chung"""
    student_id: str
    term: str
    amount: Decimal = Field(..., gt=0)                           # Số tiền thanh toán (phải > 0)
    payer_name: Optional[str] = None                             # Tên người thanh toán
    payer_email: Optional[str] = None                            # Email người thanh toán
    description: Optional[str] = None                            # Mô tả thanh toán

class PaymentCreate(PaymentBase):
    """Schema để tạo payment mới (kế thừa tất cả từ PaymentBase)"""
    pass

class PaymentIntent(BaseModel):
    """Schema cho ý định thanh toán"""
    student_id: str         # Mã số sinh viên nhận thanh toán (VD: "SV001")
    payer_id: str          # Mã số sinh viên người thanh toán (VD: "SV002") - có thể = student_id nếu tự thanh toán
    term: str              # Kỳ học
    amount: Decimal        # Số tiền thanh toán
    description: Optional[str] = None       # Mô tả thanh toán

class PaymentResponse(PaymentBase):
    """Schema trả về thông tin payment đầy đủ (kế thừa PaymentBase + thêm thông tin khác)"""
    id: str                                    # ID của payment (UUID)
    payer_id: str                              # Mã số sinh viên người thanh toán
    student_name: Optional[str] = None         # Tên sinh viên
    status: PaymentStatus                      # Trạng thái hiện tại
    failure_reason: Optional[str] = None       # Lý do thất bại (nếu có)
    created_at: datetime                       # Thời gian tạo
    updated_at: datetime                       # Thời gian cập nhật cuối
    
    class Config:
        from_attributes = True  # Cho phép tạo từ SQLAlchemy model

# EXTERNAL SERVICE SCHEMAS - SCHEMA CHO CÁC SERVICE BÊN NGOÀI

class UserInfo(BaseModel):
    """Schema thông tin user từ Auth Service"""
    id: int              # ID của user trong Auth service
    username: str        # Tên đăng nhập
    full_name: str       # Họ và tên đầy đủ
    email: str           # Địa chỉ email
    phone: str           # Số điện thoại
    balance: Decimal     # Số dư tài khoản

class StudentInfo(BaseModel):
    """Schema thông tin sinh viên từ Student Service"""
    id: int                          # ID của sinh viên
    full_name: str                   # Họ tên sinh viên
    email: Optional[str] = None      # Email sinh viên

class DebtInfo(BaseModel):
    """Schema thông tin công nợ học phí từ Tuition Service"""
    id: int              # ID của công nợ
    student_id: str      # Mã số sinh viên
    term: str            # Kỳ học
    amount: Decimal      # Số tiền công nợ
    status: str          # Trạng thái công nợ

# REQUEST/RESPONSE SCHEMAS - SCHEMA CHO REQUEST VÀ RESPONSE

class PaymentListResponse(BaseModel):
    """Schema trả về danh sách payments có phân trang"""
    payments: List[PaymentResponse]    # Danh sách payments trong trang hiện tại
    total: int                         # Tổng số payments
    page: int                          # Số trang hiện tại
    size: int                          # Số items mỗi trang

class PaymentSummary(BaseModel):
    """Schema báo cáo tổng hợp payments"""
    total_payments: int      # Tổng số payments
    total_amount: Decimal    # Tổng số tiền
    success_payments: int    # Số payments thành công
    failed_payments: int     # Số payments thất bại