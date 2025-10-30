from sqlalchemy.orm import Session
from . import models, schemas, utils
import datetime 

def get_user_by_email_or_phone(db: Session, email: str, phone: str=None) -> models.User:
    """Lấy người dùng theo email hoặc số điện thoại."""
    return db.query(models.User).filter((models.User.email == email) | (models.User.phone == phone)).first()

def get_user_by_email(db: Session, email: str) -> models.User:
    """Lấy người dùng theo email."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_phone(db: Session, phone: str) -> models.User:
    """Lấy người dùng theo số điện thoại."""
    return db.query(models.User).filter(models.User.phone == phone).first()

def get_user_by_id(db: Session, id: int) -> models.User:
    """Lấy người dùng theo ID."""
    return db.query(models.User).filter(models.User.id == id).first()

def get_users(db: Session, skip:int=0, limit:int=100):
    """Lấy danh sách người dùng với phân trang."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user:schemas.UserCreate) -> models.User:
    """Tạo người dùng mới."""
    password_hash = utils.hash_password(user.password)

    db_user = models.User(
                            email=user.email, 
                            password_hash=password_hash, 
                            full_name=user.full_name,
                            status=user.status,
                            phone=user.phone,
                            role=user.role,
                            created_at=datetime.datetime.utcnow()
                        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, id: int, user_update: schemas.UserUpdate) -> models.User:
    """Cập nhật thông tin người dùng."""
    db_user = get_user_by_id(db, id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def change_password(db: Session, user: schemas.PasswordChange) -> tuple[models.User | None, str|None]:
    """Thay đổi mật khẩu người dùng."""
    db_user = get_user_by_id(db, user.id)
    if not db_user:
        return None, "Không tìm thấy user" 
    
    checkPass = utils.verify_password(user.old_password, db_user.password_hash)
    if not checkPass:
        return None, "Mật khẩu hiện tại không chính xác"

    new_password_hash = utils.hash_password(user.new_password)
    db_user.password_hash = new_password_hash
    db.commit()
    db.refresh(db_user)
    return db_user, "Đổi mật khẩu thành công"
 
 
 # ref repository function to save refresh token jti
def save_refresh_token(db: Session, user_id: int, jti: str, token: str, expires_at: datetime.datetime, device_id: str | None = None, ip: str | None = None, user_agent: str | None = None):
    """Lưu refresh token jti vào cơ sở dữ liệu."""
    token_hash = utils.sha256_hex(token)
    db_token = models.RefreshToken(
        user_id=user_id,
        jti=jti,
        token_hash=token_hash,
        expires_at=expires_at,
        device_id=device_id,
        ip=ip,
        user_agent=user_agent,
        created_at=datetime.datetime.utcnow(), 
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
     
def get_refresh_token_by_jti(db: Session, jti: str) -> models.RefreshToken:
    """Lấy refresh token theo jti."""
    return db.query(models.RefreshToken).filter(models.RefreshToken.jti == jti).first()

def revoke_refresh_token(db: Session, jti: str) -> bool:
    """Thu hồi (revoke) refresh token theo jti."""
    db_token = get_refresh_token_by_jti(db, jti)
    if not db_token:
        return False
    db_token.revoked_at = datetime.datetime.utcnow()
    db.commit()
    return True

def revoke_all_refresh_tokens_for_user(db: Session, user_id: int) -> int:
    """Thu hồi tất cả refresh token cho một người dùng. Trả về số lượng token đã bị thu hồi."""
    tokens = db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == user_id,
        models.RefreshToken.revoked_at == None
    ).all()
    count = 0
    for token in tokens:
        token.revoked_at = datetime.datetime.utcnow()
        count += 1
    db.commit()
    return count

def rotate_refresh_token(db: Session, old_jti: str, new_jti: str, new_token: str, new_expires_at: datetime.datetime, device_id: str | None, ip: str | None, user_agent: str | None) -> bool:
    """Xoay vòng (rotate) refresh token."""
    old_token = get_refresh_token_by_jti(db, old_jti)
    if not old_token or old_token.revoked_at is not None:
        return False
    
    # Thu hồi token cũ
    old_token.revoked_at = datetime.datetime.utcnow()
    old_token.rotated_to = new_jti
    
    # Tạo token mới
    new_db_token = models.RefreshToken(
        user_id=old_token.user_id,
        jti=new_jti,
        token_hash=utils.sha256_hex(new_token),
        expires_at=new_expires_at,
        device_id=old_token.device_id,
        ip=old_token.ip,
        user_agent=old_token.user_agent,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_db_token)
    db.commit()
    return True