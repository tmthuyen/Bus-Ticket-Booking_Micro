from sqlalchemy.orm import Session
from . import models
from decimal import Decimal
import uuid

def create_payment(db: Session, booking_id, amount, method, description=None):
    """Tạo một payment mới"""
    db_payment = models.Payment(
        id=str(uuid.uuid4()),
        booking_id=str(booking_id),
        amount=Decimal(amount).quantize(Decimal('0.01')), 
        method=method,
        description=description
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: str):
    """Lấy thông tin payment theo ID"""
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()
  
