
from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta
from typing import Annotated 

from . import repository, models, schemas, utils, response
from .database import SessionLocal, engine
from .config import settings  
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
]
# Khởi tạo ứng dụng FastAPI với thông tin cơ bản
app = FastAPI(
    title="Auth Service",  # Tên service
    description="Service xử lý thông tin người dùng",  # Mô tả
    version="2.0.0",  # Phiên bản 
    docs_url="/users/docs",  # Swagger UI path
    redoc_url="/users/redoc",  # ReDoc path
    openapi_tags=tags_metadata,  # Thêm thẻ (tags) cho OpenAPI
)

app.add_middleware( # cau hinh CORS
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn (có thể thay đổi để chỉ cho phép một số nguồn cụ thể)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các tiêu đề
)

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

# Authentication function
def authenticate_user(username: str, password: str, db:Session=Depends(get_db)):
    """Xác thực người dùng bằng tên đăng nhập và mật khẩu."""
    user = repository.get_user(db, username)
    
    if not user:
        return False
    if not utils.verify_password(password, user.password_hash):
        return False
    return user

# Lấy thông tin người dùng hiện tại từ token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Lấy thông tin người dùng hiện tại từ token."""
    credentials_exception =  response.errorResponse(msg="Không thể xác thực thông tin đăng nhập", 
                                                    headers={"WWW-Authenticate": "Bearer"} )
    username = ""
    try:
        payload = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        username = payload.get("sub")   
        if username is None:
            return credentials_exception
    except JWTError:
        return credentials_exception 
    user = repository.get_user(db, username) 

    if user is None:
        return credentials_exception
    return user

# Định nghĩa các endpoint cho ứng dụng FastAPI
# Endpoint để lấy token truy cập
@app.post("/login", tags=["users"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) :
    """Đăng nhập và lấy token truy cập."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return response.errorResponse(msg="Sai tài khoản hoặc mật khẩu")
    
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = utils.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return response.successResponse(
        headers={"Content-type": "application/json", "Authorization": f"Bearer {access_token}"},
        msg="Đăng nhập thành công",
        data={
                "access_token": access_token,
                "token_type": "bearer"
            }
    ) 

# Endpoint để lấy thông tin người dùng hiện tại
@app.get("/users/me", tags=["users"])
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    """Lấy thông tin người dùng hiện tại."""
    return response.successResponse(msg="Lấy thông tin tài khoản thành công", 
                                    data=schemas.User.model_validate(current_user).model_dump())

# Endpoint để chỉnh sửa thông tin người dùng
@app.put("/{username}/edit", tags=["users"])
def edit_user(
    username: str,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    """Chỉnh sửa thông tin người dùng."""
    db_user = repository.update_user(db, username, user_update)
    if not db_user:
        return response.errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy user"
        )

    return response.successResponse( status_code=status.HTTP_202_ACCEPTED, msg="Cập nhật tài khoản thành công", 
                                    data=schemas.User.model_validate(db_user).model_dump()
                                     )
         
# Endpoint để lấy danh sách người dùng         
@app.get("/all", tags=["users"])
def get_users(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    """Lấy danh sách người dùng."""
    users = repository.get_users(db, skip=skip, limit=limit)
    return response.successResponse(msg="Lấy danh sách user thành công",
                                     data=jsonable_encoder([schemas.User.model_validate(u).model_dump() for u in users])
                                        )

# Endpoint để tạo người dùng mới
@app.post("/", response_model=schemas.User, tags=["users"])
def post_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # db_user = repository.get_user_by_email(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return repository.create_user(db=db,user=user)

# Endpoint để lấy thông tin người dùng theo username
@app.get("/{username}/detail", response_model=schemas.User, tags=["users"]) # get user by username
def get_user(username, db:Session=Depends(get_db)):
    db_user = repository.get_user(db,username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
