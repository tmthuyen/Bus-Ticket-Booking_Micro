# Background Scheduler for Auto-Cancel Expired Bookings
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from . import models, repository
from .database import SessionLocal


producer = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def set_producer(producer_instance):
    """Set global producer instance from main.py"""
    global producer
    producer = producer_instance


def auto_cancel_expired_bookings():
    """
    Background task: Tự động hủy các booking đã hết thời gian giữ chỗ
    Chạy định kỳ mỗi phút
    """
    db: Session = SessionLocal()
    try:
        current_time = datetime.now(timezone.utc)
        
        # Tìm tất cả booking PENDING đã hết hạn
        expired_bookings = db.query(models.Booking).filter(
            models.Booking.status == models.BookingStatus.PENDING,
            models.Booking.hold_until.isnot(None),
            models.Booking.hold_until < current_time
        ).all()
        
        if not expired_bookings:
            logger.info("=== No expired bookings found ===")
            return
        
        logger.info(f"Found {len(expired_bookings)} expired bookings")
        
        # Hủy từng booking
        cancelled_count = 0
        for booking in expired_bookings:
            try:
                # Hủy booking
                booking_update = repository.cancel_booking(db, booking.id)
                logger.info(f"Auto-cancelled booking {booking.booking_code} (expired at {booking.hold_until})")
                cancelled_count += 1
                
                # Gửi email thông báo qua RabbitMQ (nếu producer đã được khởi tạo)
                global producer
                if producer and producer.channel:
                    try:
                        producer.publish_booking_cancellation(
                            to_email=booking_update.email,
                            booking_code=booking_update.booking_code,
                            customer_name=booking_update.full_name,
                            cancellation_reason="Thời gian giữ chỗ đã hết hạn"
                        )
                        logger.info(f"✅Sent cancellation notification for booking {booking.booking_code}")
                    except Exception as e:
                        logger.error(f"❌Failed to send cancellation notification for booking {booking.booking_code}: {e}")
                
            except Exception as e:
                logger.error(f"❌Failed to cancel booking {booking.booking_code}: {e}")
                db.rollback()
        
        logger.info(f"✅Successfully cancelled {cancelled_count}/{len(expired_bookings)} expired bookings")
        
    except Exception as e:
        logger.error(f"❌Error in auto_cancel_expired_bookings: {e}")
    finally:
        db.close()
