from sqlalchemy.orm import Session
from . import models, schemas, utils
import datetime 

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip:int=0, limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user:schemas.UserCreate):
    password_hash = utils.hash_password(user.password)

    db_user = models.User(username=user.username, 
                            email=user.email, 
                            password_hash=password_hash, 
                            full_name=user.full_name,
                            role=user.role,
                            created_at=datetime.datetime.utcnow()
                        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, username: str, user_update: schemas.UserUpdate): 
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return None

    # Nếu muốn đổi mật khẩu
    if user_update.password is not None:
        db_user.password_hash = utils.hash_password(user_update.password)
 
    if user_update.status is not None:
        db_user.status = user_update.status

    # Ví dụ cho phép update balance
    if user_update.balance is not None:
        db_user.balance = user_update.balance
 
    db.commit()
    db.refresh(db_user)
    return db_user