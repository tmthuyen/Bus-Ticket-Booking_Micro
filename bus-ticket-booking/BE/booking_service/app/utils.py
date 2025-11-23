from datetime import datetime, timezone, timedelta
import random
import string
import re
from typing import List
from .config import settings

def generate_booking_code() -> str:
    """
    Tạo mã booking code duy nhất
    Format: BK + timestamp(6 số) + random(4 ký tự)
    Ví dụ: BK161125ABCD
    """
    # Lấy timestamp (6 chữ số: ddmmyy)
    timestamp = datetime.now().strftime("%d%m%y")
    
    # Tạo 4 ký tự random (chữ in hoa + số)
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    return f"BK{timestamp}{random_chars}"

def is_valid_email(email: str) -> bool:
    """Kiểm tra email hợp lệ"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    """Kiểm tra số điện thoại hợp lệ (10-15 ký tự số)"""
    pattern = r'^\d{10,15}$'
    return re.match(pattern, phone) is not None

def is_valid_seat_number(seat_number: str) -> bool:
    """
    Kiểm tra seat_number hợp lệ
    Format: A1, B2, C10, ... (chữ cái + số)
    """
    pattern = r'^[A-Z]\d{1,2}$'
    return re.match(pattern, seat_number.upper()) is not None

def is_valid_booking_data(
    full_name: str, 
    phone: str, 
    email: str,
    trip_id: int,
    seat_numbers: List[str],
    total_price: float
) -> tuple[bool, str]:
    """
    Kiểm tra dữ liệu booking hợp lệ
    Returns: (is_valid, error_message)
    """
    # Kiểm tra họ tên
    if not full_name or len(full_name.strip()) < 1:
        return False, "Họ tên không được để trống"
    
    if len(full_name) > 100:
        return False, "Họ tên không được quá 100 ký tự"
    
    # Kiểm tra số điện thoại
    if not phone or not is_valid_phone(phone):
        return False, "Số điện thoại không hợp lệ (10-15 chữ số)"
    
    # Kiểm tra email
    if not email or not is_valid_email(email):
        return False, "Email không hợp lệ"
    
    # Kiểm tra trip_id
    if trip_id <= 0:
        return False, "ID chuyến xe không hợp lệ"
    
    # Kiểm tra danh sách ghế
    if not seat_numbers or len(seat_numbers) == 0:
        return False, "Vui lòng chọn ít nhất 1 ghế"
    
    # Kiểm tra format từng seat_number
    for seat in seat_numbers:
        if not is_valid_seat_number(seat):
            return False, f"Số ghế '{seat}' không hợp lệ (format: A1, B2, ...)"
    
    # Kiểm tra ghế trùng lặp
    if len(seat_numbers) != len(set(seat_numbers)):
        return False, "Danh sách ghế có ghế trùng lặp"
    
    # Kiểm tra giá vé
    if total_price <= 0:
        return False, "Giá vé phải lớn hơn 0"
    
    return True, ""


def get_current_datetime() -> datetime:
    """Lấy thời gian hiện tại (UTC)"""
    return datetime.utcnow()

def format_datetime(dt: datetime, format_str: str = "%d/%m/%Y %H:%M:%S") -> str:
    """Format datetime thành string"""
    return dt.strftime(format_str)

def can_cancel_booking(booking_time: datetime, hours_before: int = 24) -> bool:
    """
    Kiểm tra có thể hủy vé không (theo chính sách hủy vé)
    Mặc định: có thể hủy trước 24 giờ
    """
    current_time = get_current_datetime()
    time_diff = booking_time - current_time
    return time_diff.total_seconds() >= (hours_before * 3600)

