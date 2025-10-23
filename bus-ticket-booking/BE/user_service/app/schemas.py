from pydantic import BaseModel, EmailStr 
from typing import Optional
from datetime import datetime
# dinh nghia INPUT, OUTPUT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None
    
class UserLogin(BaseModel): 
    username: str
    password: str

class UserUpdate(BaseModel): 
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    status: Optional[str] = None
    balance: Optional[float] = None

class UserBase(BaseModel): 
    username: str
    full_name: str 
    email: Optional[EmailStr] = None
    phone: str
    # role: Optional[str] = None
    # address: Optional[str] = None

class UserCreate(UserBase): 
    password: str  
    
class User(UserBase):
    id: int  
    status: str
    balance: float
    created_at: Optional[datetime] = None
    
    class Config():
        from_attributes  = True
        # orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


