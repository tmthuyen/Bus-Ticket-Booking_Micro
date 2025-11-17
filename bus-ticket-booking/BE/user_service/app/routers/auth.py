
from turtle import rt
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import timedelta
from typing import Annotated 

from .. import repository, models, schemas, utils
from ..security import limiter
from ..response import successResponse, errorResponse, response_authentication
from ..database import SessionLocal, engine, get_db
from ..config import settings   

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# path /auth
router = APIRouter()


# Authentication function
def authenticate_user(username: str, password: str, db:Session=Depends(get_db)) -> tuple[schemas.UserResponse | bool, str]:
    """Xác thực người dùng bằng tên đăng nhập và mật khẩu."""
    user = repository.get_user_by_email_or_phone(db, email=username, phone=username)
    
    if not user:
        return False, "Không tìm thấy user"
    checkPass = utils.verify_password(password, user.password_hash)
    if not checkPass:
        return False, "Sai mật khẩu"
 

    if user.status.value == models.UserStatus.INACTIVE.value:
        return False, "Tài khoản của bạn không hoạt động. Vui lòng liên hệ quản trị viên."
    if user.status.value == models.UserStatus.BANNED.value:
        return False, "Tài khoản của bạn đã bị khóa. Vui lòng liên hệ quản trị viên."
    return user, "Xác thực thành công"

# Lấy thông tin người dùng hiện tại từ token
# def get_current_user(token: str, db: Session = Depends(get_db)):
#     """Lấy thông tin người dùng hiện tại từ token."""
#     credentials_exception =  errorResponse(status_code=401, msg="Không thể xác thực thông tin đăng nhập", 
#                                                     headers={"WWW-Authenticate": "Bearer"} )
#     email = ""
#     try:
#         payload = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
#         email = payload.get("sub")   
#         if email is None or payload.get("scope") != "access_token":
#             return credentials_exception
#     except JWTError:
#         return credentials_exception
#     user = repository.get_user_by_email(db, email=email)

#     if user is None:
#         return credentials_exception
#     return user

# Định nghĩa các endpoint cho ứng dụng FastAPI
     
# Endpoint để lấy thông tin người dùng hiện tại
@router.get("/me", tags=["auth"])
def read_users_me(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    """Lấy thông tin người dùng hiện tại."""
    credentials_exception =  errorResponse(
        status_code=401, 
        msg="Không thể xác thực thông tin đăng nhập", 
        headers={"WWW-Authenticate": "Bearer"} 
    )
    email = ""
    token = None
    authorization_header = request.headers.get("Authorization")
    if authorization_header:
        token = authorization_header.removeprefix("Bearer ").strip()
    if not token:
        return response_authentication(
            response=response,
            status_code=401, 
            msg="Không có token truy cập", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")   
        if email is None or payload.get("scope") != "access_token":
            return credentials_exception
    except ExpiredSignatureError:
        return response_authentication(
            response=response,
            status_code=401, 
            msg="Access token đã hết hạn", 
            headers={"WWW-Authenticate": "Bearer"} 
        )
    except JWTError:
        return credentials_exception
    
    user = repository.get_user_by_email(db, email=email)
    if user is None:
        return credentials_exception
    
    current_user = schemas.UserResponse.model_validate(user).model_dump()
    return successResponse(
        msg="Lấy thông tin tài khoản thành công", 
        data=current_user
    )

# Endpoint để đăng ký người dùng mới
@router.post("/register", tags=["auth"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Đăng ký người dùng mới.""" 
    
    is_valid, msg = utils.is_valid_input_user(user, is_create=True)
    if not is_valid:
        return errorResponse(msg=msg) 
    
    db_user = repository.get_user_by_email(db, email=user.email)
    
    if db_user:
        return errorResponse(msg="Email đã được đăng ký")
    if user.phone:
        db_user = repository.get_user_by_phone(db, phone=user.phone)
        if db_user:
            return errorResponse(msg="Số điện thoại đã được đăng ký")
        
    created_user = repository.create_user(db=db, user=user)
    return successResponse(
        status_code=status.HTTP_201_CREATED,
        msg="Đăng ký tài khoản thành công",
        data=schemas.UserResponse.model_validate(created_user).model_dump()
    )


REFRESH_COOKIE_NAME = "refresh_token"    # cookie HttpOnly
CSRF_COOKIE_NAME = "csrf_token"          # chống CSRF khi dùng cookie
# Endpoint để lấy token truy cập
@router.post("/login", tags=["auth"])
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) :
    """Đăng nhập và lấy token truy cập."""
    #  Giới hạn tần suất đăng nhập theo IP
    client_ip = request.client.host if hasattr(request, "client") else "unknown"
    if not limiter.allow(client_ip):
        return errorResponse(status_code=429, msg="Quá nhiều yêu cầu đăng nhập. Vui lòng thử lại sau.")
    
    if utils.is_empty(form_data.username) or utils.is_empty(form_data.password):
        return errorResponse(msg="Tên đăng nhập và mật khẩu không được để trống")
    if not utils.is_valid_gmail(form_data.username) and not utils.is_valid_phone_number(form_data.username):
        return errorResponse(msg="Tên đăng nhập phải là email hoặc số điện thoại hợp lệ")
    
    user, message = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return errorResponse(status_code=404, msg=message)
 
    
    access_token = utils.create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_minutes=settings.jwt_expire_minutes, extra={"scope": "access_token"}
    )
    jti = utils.new_jti()
    refresh_token = utils.create_access_token(
        data={"sub": user.email, "role": user.role.value}, 
        expires_minutes=settings.jwt_refresh_expire_minutes, 
        extra={"scope": "refresh_token", "jti": jti}
    )
    response.set_cookie(
        key=REFRESH_COOKIE_NAME, value=refresh_token, 
        httponly=True, secure=False, samesite="lax", 
        max_age=settings.jwt_refresh_expire_minutes*60, path="/")

    csrf_token = utils.create_access_token(
        data={"sub": user.email}, expires_minutes=settings.jwt_refresh_expire_minutes*60, extra={"scope": "csrf_token"}
    )
    response.set_cookie(
        key=CSRF_COOKIE_NAME, value=csrf_token, 
        httponly=False, secure=False, samesite="lax", 
        max_age=settings.jwt_refresh_expire_minutes * 60, path="/")
    
    # print(form_data)
    # Lưu refresh token jti vào cơ sở dữ liệu hoặc bộ nhớ đệm nếu cần thiết (bỏ qua trong ví dụ này)
    repository.save_refresh_token(
        db, 
        user_id=user.id, 
        jti=jti,
        token=refresh_token,
        expires_at=utils.add_seconds(utils.now_utc(), settings.jwt_refresh_expire_minutes*60),
        device_id=request.headers.get("Device-ID") or "unknown",
        ip=request.client.host if hasattr(request, "client") else None,
        user_agent=request.headers.get("User-Agent"),
    )


    return response_authentication(
        response=response,
        headers={"Content-type": "application/json", "Authorization": f"Bearer {access_token}"},
        msg="Đăng nhập thành công",
        data={
                "access_token": access_token, 
                "token_type": "bearer"
            }, 
        
    ) 
    
# Endpoint để refresh token truy cập
@router.post("/token/refresh", tags=["auth"])  
def refresh_access_token(
    req: Request, res: Response, db: Session = Depends(get_db)
):
    """Làm mới token truy cập."""
    refresh_token = req.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        return errorResponse(status_code=401, msg="Không tìm thấy refresh token")
    
    # Kiem tra CSRF header
    csrf_header = req.headers.get("X-CSRF-Token")
    csrf_cookie = req.cookies.get(CSRF_COOKIE_NAME)
    if not csrf_header or not csrf_cookie or csrf_header != csrf_cookie:
        return errorResponse(status_code=403, msg="Yêu cầu không hợp lệ (CSRF token không hợp lệ)")
    
    # decode refresh token
    try:
        payload = jwt.decode(refresh_token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        scope: str = payload.get("scope")
        if scope != "refresh_token":
            return errorResponse(status_code=401, msg="Refresh token không hợp lệ")
    except ExpiredSignatureError:
        #  Revoke token da het han
        try:
            # Giải mã bỏ qua exp để lấy jti/email phục vụ revoke/audit
            payload = jwt.decode(
                refresh_token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm],
                options={"verify_exp": False}
            )
            jti = payload.get("jti")
            if jti:
                repository.revoke_refresh_token(db, jti)  # đánh dấu revoked trong DB
        except Exception:
            pass

        # Xoá cookie (dùng đúng path bạn set khi login, ví dụ "/")
        res.delete_cookie(REFRESH_COOKIE_NAME, path="/")
        res.delete_cookie(CSRF_COOKIE_NAME, path="/")
        return errorResponse(status_code=401, msg="Refresh token đã hết hạn")
    except JWTError:
        return errorResponse(status_code=401, msg="Refresh token không hợp lệ")
    
    email: str = payload.get("sub")
    jti = payload.get("jti")
    if email is None or jti is None:
        return errorResponse(status_code=401, msg="Refresh token không hợp lệ")
    
    find_refresh_token = repository.get_refresh_token_by_jti(db, jti)
    if not find_refresh_token:
        return errorResponse(status_code=401, msg="Refresh token không hợp lệ")
    
    if find_refresh_token.revoked_at is not None or find_refresh_token.expires_at < utils.now_utc():
        return errorResponse(status_code=401, msg="Refresh token không còn hiệu lực")
    
    if not utils.consteq(find_refresh_token.token_hash, utils.sha256_hex(refresh_token)):
        return errorResponse(status_code=401, msg="Refresh token không hợp lệ")
    
    # =======Rotate refresh token=======
    # Token moi
    new_access_token = utils.create_access_token(
        data={"sub": email, "role": payload.get("role")}, expires_minutes=settings.jwt_expire_minutes, extra={"scope": "access_token"}
    )
    new_jti = utils.new_jti()
    new_refresh_token = utils.create_access_token(
        data={"sub": email, "role": payload.get("role")}, 
        expires_minutes=settings.jwt_refresh_expire_minutes, 
        extra={"scope": "refresh_token", "jti": new_jti}
    )
    
    """
        Rotate refresh token (mỗi lần /refresh thì cấp refresh token mới, 
        vô hiệu hoá cái cũ) để chặn replay và cho phép thu hồi phiên an toàn. 
        Nếu không rotate, ai cầm được refresh token cũ 
        có thể “vắt” access token mãi tới khi refresh
    """
    repository.rotate_refresh_token(
        db,
        old_jti=jti,
        new_jti=new_jti,
        new_token=new_refresh_token,
        new_expires_at=utils.add_seconds(utils.now_utc(), settings.jwt_refresh_expire_minutes*60),
        device_id=find_refresh_token.device_id,
        ip=find_refresh_token.ip,
        user_agent=find_refresh_token.user_agent
    )
    
    # set cookie refresh token moi
    res.set_cookie(
        key=REFRESH_COOKIE_NAME, value=new_refresh_token, 
        httponly=True, secure=False, samesite="lax", 
        max_age=settings.jwt_refresh_expire_minutes*60, path="/"
    )

    return response_authentication(
        response=res,
        msg="Làm mới access token thành công",
        data={
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    )

@router.post("/logout", tags=["auth"])
def logout_user(req: Request, res: Response, db: Session = Depends(get_db)):
    """Đăng xuất người dùng."""
    refresh_access_token = req.cookies.get(REFRESH_COOKIE_NAME)
    
    if refresh_access_token:
        try:
            payload = jwt.decode(refresh_access_token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            jti: str = payload.get("jti")
            if jti:
                repository.revoke_refresh_token(db, jti)
        except JWTError:
            pass  # Nếu token không hợp lệ, bỏ qua
    
    res.delete_cookie(REFRESH_COOKIE_NAME, path="/")
    res.delete_cookie(CSRF_COOKIE_NAME, path="/")
    return response_authentication(
        response=res,
        msg="Đăng xuất thành công"
    )
