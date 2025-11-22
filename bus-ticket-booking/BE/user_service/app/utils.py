from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import jwt 
import re
import uuid, hmac, hashlib

from . import schemas
from .models import UserStatus, UserRole
from .config import settings
# Regex để kiểm tra phần local của địa chỉ Gmail
_GMAIL_LOCAL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+$")
ALLOWED_GMAIL_DOMAINS = ["gmail.com", "googlemail.com"]

# Khởi tạo CryptContext để hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hàm tiện ích

def is_valid_gmail(addr: str) -> bool:
    """
    Trả về True nếu addr là địa chỉ Gmail hợp lệ (gmail.com hoặc googlemail.com).
    Quy tắc chính:
      - Có đúng 1 ký tự '@'
      - Domain ∈ {gmail.com, googlemail.com} (không phân biệt hoa/thường)
      - local-part dài 1..64, toàn bộ địa chỉ ≤ 254 ký tự
      - local-part chỉ chứa [A-Za-z0-9._%+-]
      - Không bắt đầu/kết thúc bằng '.', không có '..' liên tiếp
    """
    if not isinstance(addr, str):
        return False
    if len(addr) > 254:
        return False

    parts = addr.split("@")
    if len(parts) != 2:
        return False

    local, domain = parts[0], parts[1].lower()

    if domain not in ALLOWED_GMAIL_DOMAINS:
        return False
    if not (1 <= len(local) <= 64):
        return False
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    if not _GMAIL_LOCAL_RE.fullmatch(local):
        return False
    return True

def is_valid_phone_number(phone: str) -> bool:
    """
    Kiểm tra xem chuỗi phone có phải là số điện thoại Việt Nam hợp lệ hay không.
    Quy tắc:
      - Bắt đầu bằng '0'
      - Tiếp theo là 9 hoặc 10 chữ số (tổng cộng 10 hoặc 11 chữ số)
    """
    if not isinstance(phone, str):
        return False
    pattern = r"^0\d{9,10}$"
    return re.fullmatch(pattern, phone) is not None

def is_valid_password(password: str) -> bool:
    """
    Kiểm tra xem mật khẩu có hợp lệ hay không.
    Quy tắc:
      - Ít nhất 8 ký tự
      - Chứa ít nhất một chữ cái viết hoa
      - Chứa ít nhất một chữ cái viết thường
      - Chứa ít nhất một chữ số
      - Chứa ít nhất một ký tự đặc biệt (!@#$%^&*()-+)
    """
    if not isinstance(password, str):
        return False
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*()\-\+]", password):
        return False
    return True

def is_empty(s: str | None) -> bool:
    """Kiểm tra chuỗi s có rỗng hoặc chỉ chứa khoảng trắng hay không."""
    return s is None or s.strip() == ""

def is_valid_input_user(user: schemas.UserCreate | schemas.UserUpdate, is_create: bool=True) -> tuple[bool, str]:
    """
    Kiểm tra tính hợp lệ của thông tin người dùng.
    Yêu cầu:
      - 'email' hoặc 'phone' phải có và hợp lệ
      - 'password' phải có và hợp lệ
    """ 
    
    if is_create:
        if is_empty(user.email) or is_empty(user.full_name):
            return False, "Email và họ tên không được để trống"
        
        if not is_valid_gmail(user.email):
            return False, "Email không hợp lệ. Vui lòng sử dụng địa chỉ Gmail."
        
        if user.password != user.confirm_password:
            return False, "Mật khẩu và mật khẩu xác nhận không khớp."
        
        if is_valid_password(user.password) is False:
            return False, "Mật khẩu không hợp lệ. Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt."

    # Kiem tra cap nhat
    else:
        if not is_empty(user.email) and not is_valid_gmail(user.email):
            return False, "Email không hợp lệ. Vui lòng sử dụng địa chỉ Gmail."
        
        if not is_empty(user.phone) and not is_valid_phone_number(user.phone):
            return False, "Số điện thoại không hợp lệ."
        
        if is_empty(user.full_name):
            return False, "Họ tên không được để trống."
        
    if not is_empty(user.role) and user.role not in [role.value for role in UserRole]:
        return False, "Vai trò người dùng không hợp lệ."
    if not is_empty(user.status) and user.status not in [status.value for status in UserStatus]:
        return False, "Trạng thái người dùng không hợp lệ."
    return True, "Dữ liệu hợp lệ."

# auth utils
def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def consteq(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)

def new_jti() -> str:
    return str(uuid.uuid4())


def hash_password(password: str) -> str:
    """Băm (hash) mật khẩu người dùng."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Xác thực mật khẩu người dùng."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_minutes: int, extra: dict | None = None):
    """Tạo JWT access token."""
    now = datetime.now(timezone.utc)
    payload = data.copy()
    expire = now + timedelta(minutes=expires_minutes)
    payload.update({"exp": expire})
    payload.update({"iat": int(now.timestamp())})
    payload.update(extra or {})
    encoded_jwt = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def add_seconds(ts: datetime, seconds: int) -> datetime:
    return ts + timedelta(seconds=seconds)