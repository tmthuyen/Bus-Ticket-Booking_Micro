from pydantic import BaseModel, ConfigDict, EmailStr 
from typing import Optional
from datetime import datetime
from . import models
# dinh nghia INPUT, OUTPUT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None
    
class UserLogin(BaseModel): 
    email: str
    password: str

class UserBase(BaseModel):
    email: str = None
    full_name: str = None
    phone: Optional[str] = None
    status: Optional[str] = models.UserStatus.ACTIVE.value
    role: Optional[str] = models.UserRole.CUSTOMER.value

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserUpdate(UserBase): 
    pass
    
class PasswordChange(BaseModel):
    id: int
    old_password: str
    new_password: str
    confirm_password: str
    
class UserResponse(UserBase):
    id: int
    # v2: thay cho orm_mode = True
    model_config = ConfigDict(from_attributes=True)

    
 