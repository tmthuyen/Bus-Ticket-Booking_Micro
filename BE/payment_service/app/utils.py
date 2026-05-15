import hashlib
import hmac
import json
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Any, Optional
import re

def generate_order_id(prefix: str = "PAY") -> str:
    """Tạo order ID unique"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = str(uuid.uuid4())[:8].upper()
    return f"{prefix}{timestamp}{random_suffix}"

def generate_request_id() -> str:
    """Tạo request ID cho MoMo"""
    return str(uuid.uuid4())

def create_hmac_signature(secret_key: str, data: str) -> str:
    """Tạo HMAC SHA256 signature"""
    return hmac.new(
        secret_key.encode('utf-8'),
        data.encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()

def format_currency(amount: Decimal) -> str:
    """Format số tiền theo định dạng VND"""
    return f"{amount:,.0f} VND"

def validate_phone_number(phone: str) -> bool:
    """Validate số điện thoại Việt Nam"""
    pattern = r'^(\+84|0)(3|5|7|8|9)[0-9]{8}$'
    return bool(re.match(pattern, phone))

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def parse_json_safely(json_str: str) -> Optional[Dict[str, Any]]:
    """Parse JSON string safely"""
    try:
        return json.loads(json_str) if json_str else None
    except (json.JSONDecodeError, TypeError):
        return None

def serialize_json(data: Dict[str, Any]) -> str:
    """Serialize dict to JSON string"""
    try:
        return json.dumps(data, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return "{}"

def calculate_expiry_time(minutes: int = 15) -> datetime:
    """Tính thời gian hết hạn (mặc định 15 phút)"""
    return datetime.utcnow() + timedelta(minutes=minutes)

def is_expired(expiry_time: datetime) -> bool:
    """Kiểm tra đã hết hạn chưa"""
    return datetime.utcnow() > expiry_time

def mask_sensitive_data(data: str, show_chars: int = 4) -> str:
    """Che dấu thông tin nhạy cảm"""
    if len(data) <= show_chars * 2:
        return "*" * len(data)
    return data[:show_chars] + "*" * (len(data) - show_chars * 2) + data[-show_chars:]

class MoMoUtils:
    """Utility class cho MoMo operations"""
    @staticmethod
    # ✅ FIXED: Proper signature string construction
    def build_raw_signature(**kwargs) -> str:
        """Build signature string theo đúng format MoMo"""
        # MoMo yêu cầu thứ tự cụ thể
        signature_string = (
            f"accessKey={kwargs['accessKey']}&"
            f"amount={kwargs['amount']}&"
            f"extraData={kwargs['extraData']}&"
            f"ipnUrl={kwargs['ipnUrl']}&"
            f"orderId={kwargs['orderId']}&"
            f"orderInfo={kwargs['orderInfo']}&"
            f"partnerCode={kwargs['partnerCode']}&"
            f"redirectUrl={kwargs['redirectUrl']}&"
            f"requestId={kwargs['requestId']}&"
            f"requestType={kwargs['requestType']}"
        )
        return signature_string
    
    @staticmethod
    def verify_momo_signature(raw_signature: str, signature: str, secret_key: str) -> bool:
        """Verify MoMo signature"""
        expected_signature = create_hmac_signature(secret_key, raw_signature)
        return hmac.compare_digest(expected_signature, signature)
    
    @staticmethod
    def parse_momo_result_code(result_code: int) -> tuple[str, str]:
        """Parse MoMo result code thành status và message"""
        momo_codes = {
            0: ("success", "Giao dịch thành công"),
            9000: ("failed", "Giao dịch không thành công"),
            8000: ("failed", "Giao dịch đang được xử lý"),
            7000: ("failed", "Trừ tiền thành công. Giao dịch bị nghi ngờ (Server xử lý timeout)"),
            1000: ("failed", "Giao dịch được khởi tạo, chờ người dùng xác nhận thanh toán"),
            4001: ("failed", "Số dư không đủ để thực hiện giao dịch"),
            4100: ("failed", "Giao dịch bị từ chối"),
        }
        
        return momo_codes.get(result_code, ("failed", f"Lỗi không xác định: {result_code}"))

def log_payment_event(payment_id: str, event_type: str, event_data: Dict[str, Any] = None):
    """Helper để log payment events (sẽ được gọi từ repository)"""
    return {
        "payment_id": payment_id,
        "event_type": event_type,
        "event_data": serialize_json(event_data or {}),
        "timestamp": datetime.utcnow().isoformat()
    }

# Constants
MOMO_RESULT_CODES = {
    0: "Thành công",
    9000: "Giao dịch không thành công", 
    8000: "Giao dịch đang được xử lý",
    7000: "Trừ tiền thành công. Giao dịch bị nghi ngờ",
    1000: "Giao dịch được khởi tạo, chờ người dùng xác nhận",
    4001: "Số dư không đủ",
    4100: "Giao dịch bị từ chối"
}

# Validation patterns
PHONE_PATTERN = r'^(\+84|0)(3|5|7|8|9)[0-9]{8}$'
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'