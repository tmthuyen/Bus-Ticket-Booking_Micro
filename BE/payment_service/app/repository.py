from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_, or_
from typing import Optional, List
from decimal import Decimal
import uuid
from datetime import datetime

from . import models
from .models import Payment, PaymentLog, PaymentStatus, PaymentMethod, PaymentEventType

# ===== PAYMENT OPERATIONS =====

def create_payment(
    db: Session, 
    booking_id: str, 
    amount: Decimal, 
    method: PaymentMethod, 
    description: Optional[str] = None
) -> Payment:
    """Tạo một payment mới"""
    db_payment = Payment(
        id=str(uuid.uuid4()),
        booking_id=str(booking_id),
        amount=Decimal(str(amount)).quantize(Decimal('0.01')), 
        method=method,
        description=description,
        status=PaymentStatus.PENDING
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: str) -> Optional[Payment]:
    """Lấy thông tin payment theo ID"""
    return db.query(Payment).filter(Payment.id == payment_id).first()

def get_payment_by_booking_id(db: Session, booking_id: str) -> Optional[Payment]:
    """Lấy payment theo booking_id"""
    return db.query(Payment).filter(Payment.booking_id == booking_id).first()

def get_payment_by_provider_transaction_id(db: Session, provider_transaction_id: str) -> Optional[Payment]:
    """Lấy payment theo provider transaction ID (order_id từ MoMo)"""
    return db.query(Payment).filter(
        Payment.provider_transaction_id == provider_transaction_id
    ).first()

def get_payments_by_status(db: Session, status: PaymentStatus, limit: int = 100) -> List[Payment]:
    """Lấy danh sách payments theo status"""
    return db.query(Payment).filter(
        Payment.status == status
    ).order_by(desc(Payment.created_at)).limit(limit).all()

def get_payments_by_method(db: Session, method: PaymentMethod, limit: int = 100) -> List[Payment]:
    """Lấy danh sách payments theo method"""
    return db.query(Payment).filter(
        Payment.method == method
    ).order_by(desc(Payment.created_at)).limit(limit).all()

def update_payment_status(
    db: Session, 
    payment_id: str, 
    status: PaymentStatus,
    provider_transaction_id: Optional[str] = None,
    raw_response: Optional[str] = None
) -> Optional[Payment]:
    """Update payment status"""
    db_payment = get_payment(db, payment_id)
    if db_payment:
        db_payment.status = status
        db_payment.updated_at = datetime.utcnow()
        
        if provider_transaction_id:
            db_payment.provider_transaction_id = provider_transaction_id
            
        if raw_response:
            db_payment.raw_response = raw_response
            
        db.commit()
        db.refresh(db_payment)
    return db_payment

def update_payment_momo_info(
    db: Session,
    payment_id: str,
    provider_transaction_id: Optional[str] = None,
    payment_info: Optional[str] = None,
    raw_response: Optional[str] = None,
    secure_hash: Optional[str] = None
) -> Optional[Payment]:
    """Update payment với thông tin MoMo"""
    db_payment = get_payment(db, payment_id)
    if db_payment:
        if provider_transaction_id:
            db_payment.provider_transaction_id = provider_transaction_id
        if payment_info:
            db_payment.payment_info = payment_info
        if raw_response:
            db_payment.raw_response = raw_response
        if secure_hash:
            db_payment.secure_hash = secure_hash
            
        db_payment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_payment)
    return db_payment

# ===== PAYMENT LOG OPERATIONS =====

def create_payment_log(
    db: Session, 
    payment_id: str, 
    event_type: PaymentEventType, 
    event_data: Optional[dict] = None
) -> PaymentLog:
    """Tạo một payment log mới"""
    from .utils import serialize_json
    
    db_log = PaymentLog(
        id=str(uuid.uuid4()),
        payment_id=payment_id,
        event_type=event_type,
        event_data=serialize_json(event_data) if event_data else None
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_payment_logs(db: Session, payment_id: str) -> List[PaymentLog]:
    """Lấy tất cả logs của một payment"""
    return db.query(PaymentLog).filter(
        PaymentLog.payment_id == payment_id
    ).order_by(desc(PaymentLog.created_at)).all()

def get_payment_logs_by_event_type(
    db: Session, 
    payment_id: str, 
    event_type: PaymentEventType
) -> List[PaymentLog]:
    """Lấy logs theo event type"""
    return db.query(PaymentLog).filter(
        and_(
            PaymentLog.payment_id == payment_id,
            PaymentLog.event_type == event_type
        )
    ).order_by(desc(PaymentLog.created_at)).all()

def get_recent_payment_logs(db: Session, limit: int = 50) -> List[PaymentLog]:
    """Lấy logs gần đây nhất"""
    return db.query(PaymentLog).order_by(
        desc(PaymentLog.created_at)
    ).limit(limit).all()

# ===== ADVANCED QUERIES =====

def get_payment_with_logs(db: Session, payment_id: str) -> Optional[Payment]:
    """Lấy payment kèm theo tất cả logs"""
    return db.query(Payment).options(
        joinedload(Payment.logs)
    ).filter(Payment.id == payment_id).first()

def get_payments_by_date_range(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    status: Optional[PaymentStatus] = None,
    method: Optional[PaymentMethod] = None
) -> List[Payment]:
    """Lấy payments trong khoảng thời gian"""
    query = db.query(Payment).filter(
        and_(
            Payment.created_at >= start_date,
            Payment.created_at <= end_date
        )
    )
    
    if status:
        query = query.filter(Payment.status == status)
    
    if method:
        query = query.filter(Payment.method == method)
    
    return query.order_by(desc(Payment.created_at)).all()

def get_payment_statistics(db: Session) -> dict:
    """Lấy thống kê payments"""
    from sqlalchemy import func
    
    total_payments = db.query(func.count(Payment.id)).scalar()
    
    success_payments = db.query(func.count(Payment.id)).filter(
        Payment.status == PaymentStatus.SUCCESS
    ).scalar()
    
    pending_payments = db.query(func.count(Payment.id)).filter(
        Payment.status == PaymentStatus.PENDING
    ).scalar()
    
    failed_payments = db.query(func.count(Payment.id)).filter(
        Payment.status == PaymentStatus.FAILED
    ).scalar()
    
    total_amount = db.query(func.sum(Payment.amount)).filter(
        Payment.status == PaymentStatus.SUCCESS
    ).scalar() or 0
    
    momo_payments = db.query(func.count(Payment.id)).filter(
        Payment.method == PaymentMethod.MOMO
    ).scalar()
    
    return {
        "total_payments": total_payments,
        "success_payments": success_payments,
        "pending_payments": pending_payments,
        "failed_payments": failed_payments,
        "total_amount": float(total_amount),
        "momo_payments": momo_payments,
        "success_rate": (success_payments / total_payments * 100) if total_payments > 0 else 0
    }

def search_payments(
    db: Session,
    booking_id: Optional[str] = None,
    provider_transaction_id: Optional[str] = None,
    amount_min: Optional[Decimal] = None,
    amount_max: Optional[Decimal] = None,
    status: Optional[PaymentStatus] = None,
    method: Optional[PaymentMethod] = None,
    limit: int = 50
) -> List[Payment]:
    """Tìm kiếm payments với nhiều criteria"""
    query = db.query(Payment)
    
    if booking_id:
        query = query.filter(Payment.booking_id.like(f"%{booking_id}%"))
    
    if provider_transaction_id:
        query = query.filter(Payment.provider_transaction_id.like(f"%{provider_transaction_id}%"))
    
    if amount_min:
        query = query.filter(Payment.amount >= amount_min)
    
    if amount_max:
        query = query.filter(Payment.amount <= amount_max)
    
    if status:
        query = query.filter(Payment.status == status)
    
    if method:
        query = query.filter(Payment.method == method)
    
    return query.order_by(desc(Payment.created_at)).limit(limit).all()

# ===== CLEANUP OPERATIONS =====

def delete_old_logs(db: Session, older_than_days: int = 30) -> int:
    """Xóa logs cũ hơn X ngày"""
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)
    
    deleted_count = db.query(PaymentLog).filter(
        PaymentLog.created_at < cutoff_date
    ).delete()
    
    db.commit()
    return deleted_count

def cleanup_failed_payments(db: Session, older_than_hours: int = 24) -> int:
    """Cleanup các failed payments cũ"""
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(hours=older_than_hours)
    
    deleted_count = db.query(Payment).filter(
        and_(
            Payment.status == PaymentStatus.FAILED,
            Payment.created_at < cutoff_date
        )
    ).delete()
    
    db.commit()
    return deleted_count

# ===== UTILITY FUNCTIONS =====

def payment_exists(db: Session, booking_id: str) -> bool:
    """Kiểm tra payment đã tồn tại cho booking_id"""
    return db.query(Payment).filter(Payment.booking_id == booking_id).first() is not None

def get_pending_payments_older_than(db: Session, minutes: int = 15) -> List[Payment]:
    """Lấy các pending payments cũ hơn X phút"""
    from datetime import timedelta
    
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    
    return db.query(Payment).filter(
        and_(
            Payment.status == PaymentStatus.PENDING,
            Payment.created_at < cutoff_time
        )
    ).all()