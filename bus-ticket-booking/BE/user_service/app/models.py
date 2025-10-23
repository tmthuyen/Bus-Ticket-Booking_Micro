from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum
import datetime 
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(10),unique=True)
    password_hash = Column(String(255))
    full_name = Column(String(255))
    email = Column(String(40), unique=True)
    phone = Column(String(11))
    balance = Column(Numeric(18, 3), default=0)
    status = Column(Enum('ACTIVE', 'PAYING', 'INACTIVE'), default='ACTIVE')
    role = Column(String(7), default='STUDENT')
    created_at = Column(DateTime, default=datetime.datetime.utcnow())

 