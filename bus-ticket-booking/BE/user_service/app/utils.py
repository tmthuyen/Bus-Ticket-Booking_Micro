from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import jwt

from .config import settings

# Khởi tạo CryptContext để hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hàm tiện ích
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt