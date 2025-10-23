import json
from datetime import datetime
from decimal import Decimal
from typing import Any
import uuid
import hashlib
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

VN = ZoneInfo("Asia/Ho_Chi_Minh")

def to_vn(dt: datetime) -> datetime:
    if dt.tzinfo is None:  # giả định dt đang là UTC nếu thiếu tzinfo
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(VN)

def to_vn_str(dt: datetime, fmt="%Y-%m-%d %H:%M:%S %z") -> str:
    return to_vn(dt).strftime(fmt)
 

def generate_payment_id() -> str:
    """Generate unique payment ID"""
    return str(uuid.uuid4())

def generate_idempotency_key(payer_id: int, student_id: str, term: str, amount: Decimal) -> str:
    """Generate idempotency key to prevent duplicate payments"""
    data = f"{payer_id}_{student_id}_{term}_{int(amount * 1000)}"
    return hashlib.md5(data.encode()).hexdigest()

def format_currency(amount: Decimal) -> str:
    """Format amount as Vietnamese currency"""
    return f"{amount:,.0f} VND"

def validate_student_id(student_id: str) -> bool:
    """Validate student ID format (assuming 8-digit number)"""
    return student_id.isdigit() and len(student_id) <= 10

def validate_term(term: str) -> bool:
    """Validate term format (e.g., 2024A, 2024B)"""
    if len(term) != 5:
        return False
    year = term[:4]
    semester = term[4]
    return year.isdigit() and semester in ['A', 'B', 'C']

def serialize_json(obj: Any) -> str:
    """Serialize object to JSON string with datetime handling"""
    def default_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Decimal):
            return str(o)
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    
    return json.dumps(obj, default=default_serializer)

def get_client_ip(request) -> str:
    """Get client IP from request"""
    if hasattr(request, 'client') and request.client:
        return request.client.host
    return "unknown"

def get_user_agent(request) -> str:
    """Get user agent from request"""
    if hasattr(request, 'headers'):
        return request.headers.get("user-agent", "unknown")
    return "unknown"

class PaymentError(Exception):
    """Custom payment error"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)



class InsufficientBalanceError(PaymentError):
    """Insufficient balance error"""
    pass

class DebtNotFoundError(PaymentError):
    """Debt not found error"""
    pass