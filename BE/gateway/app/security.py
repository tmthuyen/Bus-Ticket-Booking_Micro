from fastapi import Request, HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from .setting import settings

def needs_auth(path: str) -> bool:
    # print("Allowlist path:", settings.ALLOWLIST_PATHS)
    # bỏ qua các path allowlist
    # print("Checking auth for path:", path)
    return path.rstrip("/") not in settings.ALLOWLIST_PATHS

def verify_jwt(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Request thiếu Token bearer")
    token = auth.split()[1]
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except ExpiredSignatureError:
        raise HTTPException(401, "Token đã hết hạn")
    except JWTError:
        raise HTTPException(401, "Token không hợp lệ")
    
    print("Decoded JWT payload:", payload)
    if payload.get("scope") not in ("anonymous_token", "access_token"):  # chấp nhận token không gắn 'type' hoặc 'access'
        raise HTTPException(401, "Kiểu Token không hợp lệ")
    
    return payload
