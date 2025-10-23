from fastapi import Request, HTTPException
from jose import jwt, JWTError
from .setting import settings

def needs_auth(path: str) -> bool:
    # bỏ qua các path allowlist
    return path.rstrip("/") not in settings.ALLOWLIST_PATHS

def verify_jwt(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Request thiếu Authorization header")
    token = auth.split()[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError:
        raise HTTPException(401, "Token không hợp lệ hoặc đã hết hạn")
    if payload.get("type") not in (None, "access"):  # chấp nhận token không gắn 'type' hoặc 'access'
        raise HTTPException(401, "Invalid token type")
    return payload
