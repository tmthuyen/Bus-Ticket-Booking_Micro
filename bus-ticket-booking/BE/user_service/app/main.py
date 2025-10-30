
from fastapi import FastAPI, Depends, status
# from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 

from . import repository, models, schemas, utils
from .response import successResponse, errorResponse, response_authentication
from .database import engine, get_db 
from .routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
]
# Khởi tạo ứng dụng FastAPI với thông tin cơ bản
app = FastAPI(
    title="User Service",  # Tên service
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


# Include router for authentication endpoints
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Endpoint để lấy thông tin người dùng theo username
@app.get("/{username}/detail", tags=["users"]) # get user by username
def get_user(username, db:Session=Depends(get_db)):
    """Lấy thông tin người dùng theo username (email hoặc số điện thoại)."""
    db_user = repository.get_user_by_email_or_phone(db,email=username, phone=username)
    if not db_user:
        return errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy user"
        )
        
    return successResponse(msg="Lấy thông tin user thành công",
                                     data=schemas.UserResponse.model_validate(db_user).model_dump()
                                        )
    
# Endpoint để chỉnh sửa thông tin người dùng
@app.put("/{id}/edit", tags=["users"])
def edit_user(
    id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    """Chỉnh sửa thông tin người dùng."""
    if not user_update:
        return errorResponse(msg="Dữ liệu cập nhật không được để trống")
    
    is_valid, msg = utils.is_valid_input_user(user_update, is_create=False)
    if not is_valid:
        return errorResponse(msg=msg)

    db_user = repository.update_user(db, id=id, user_update=user_update)
    if not db_user:
        return errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy user"
        )

    return successResponse( status_code=status.HTTP_202_ACCEPTED, msg="Cập nhật tài khoản thành công", 
                                    data=schemas.UserResponse.model_validate(db_user).model_dump()
                                     )
         
# Endpoint để thay đổi mật khẩu
@app.post("/change-password", tags=["users"])
def change_password(
    password_change: schemas.PasswordChange, 
    db: Session = Depends(get_db),
):
    """Thay đổi mật khẩu người dùng."""
    if password_change.new_password != password_change.confirm_password:
        return errorResponse(msg="Mật khẩu xác nhận không khớp")
    if not utils.is_valid_password(password_change.new_password):
        return errorResponse(msg="Mật khẩu mới không hợp lệ")

    user = repository.get_user_by_id(db, password_change.id)
    if not user:
        return errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg="Không tìm thấy user"
        ) 

    updated_user, msg = repository.change_password(db, password_change)
    if not updated_user:
        return errorResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            msg=msg
        )
    return successResponse(
        msg=msg,
        data=schemas.UserResponse.model_validate(updated_user).model_dump()
    )

# Endpoint để lấy danh sách người dùng         
@app.get("/all", tags=["users"])
def get_users(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    """Lấy danh sách người dùng."""
    users = repository.get_users(db, skip=skip, limit=limit)
    return successResponse(msg="Lấy danh sách user thành công",
                                     data=jsonable_encoder([schemas.UserResponse.model_validate(u).model_dump() for u in users])
                                        )


    
