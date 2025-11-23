from typing import Optional, Dict, Any, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging

from ..models import Payment, PaymentLog, PaymentStatus, PaymentMethod, PaymentEventType
from ..schemas import PaymentCreate, MoMoPaymentRequest, RefundRequest
from .. import repository
from .momo_service import MoMoService
from ..utils import generate_order_id, serialize_json, log_payment_event
from ..config import settings

logger = logging.getLogger(__name__)

class PaymentService:
    """Business logic layer cho Payment Service"""
    
    def __init__(self):
        self.momo_service = MoMoService()
    
    async def create_payment(
        self, 
        db: Session, 
        payment_data: PaymentCreate
    ) -> Tuple[bool, str, Optional[Payment]]:
        """
        Tạo payment mới
        
        Args:
            db: Database session
            payment_data: Dữ liệu tạo payment
            
        Returns:
            Tuple (success, message, payment_object)
        """
        try:
            # Kiểm tra booking_id đã có payment chưa
            existing_payment = repository.get_payment_by_booking_id(
                db, str(payment_data.booking_id)
            )
            
            if existing_payment:
                return False, "Booking này đã có payment", None
            
            # Tạo payment mới
            db_payment = repository.create_payment(
                db=db,
                booking_id=str(payment_data.booking_id),
                amount=payment_data.amount,
                method=payment_data.method,
                description=payment_data.description
            )
            
            # Log event
            repository.create_payment_log(
                db=db,
                payment_id=db_payment.id,
                event_type=PaymentEventType.CREATED,
                event_data={
                    "booking_id": str(payment_data.booking_id),
                    "amount": str(payment_data.amount),
                    "method": payment_data.method.value
                }
            )
            
            logger.info(f"Created payment {db_payment.id} for booking {payment_data.booking_id}")
            
            return True, "Payment created successfully", db_payment
            
        except SQLAlchemyError as e:
            logger.error(f"Database error creating payment: {str(e)}")
            db.rollback()
            return False, "Database error", None
        except Exception as e:
            logger.error(f"Unexpected error creating payment: {str(e)}")
            db.rollback()
            return False, "Internal server error", None
    
    async def create_momo_payment(
        self,
        db: Session,
        payment_request: MoMoPaymentRequest
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Tạo thanh toán MoMo
        
        Args:
            db: Database session
            payment_request: Dữ liệu request MoMo
            
        Returns:
            Tuple (success, message, response_data)
        """
        try:
            # Tạo payment record trước
            payment_create = PaymentCreate(
                booking_id=payment_request.booking_id,
                amount=payment_request.amount,
                method=PaymentMethod.MOMO,
                description=payment_request.order_info
            )
            
            success, message, db_payment = await self.create_payment(db, payment_create)
            
            if not success:
                return False, message, None
            
            # Log bắt đầu tạo MoMo request
            repository.create_payment_log(
                db=db,
                payment_id=db_payment.id,
                event_type=PaymentEventType.REQUEST_TRANSACTION,
                event_data={
                    "provider": "momo",
                    "amount": str(payment_request.amount),
                    "order_info": payment_request.order_info
                }
            )
            
            # Tạo MoMo payment request
            momo_response = self.momo_service.create_payment_request(
                booking_id=str(payment_request.booking_id),
                amount=payment_request.amount,
                order_info=payment_request.order_info or "Thanh toán vé xe",
                customer_name=payment_request.customer_name,
                customer_phone=payment_request.customer_phone,
                payment_method=payment_request.payment_method.value if payment_request.payment_method else "credit",
                redirect_url=payment_request.redirect_url,
                ipn_url=payment_request.ipn_url
            )
            
            if not momo_response.get("success"):
                # Update payment status to failed
                repository.update_payment_status(
                    db, db_payment.id, PaymentStatus.FAILED
                )
                
                repository.create_payment_log(
                    db=db,
                    payment_id=db_payment.id,
                    event_type=PaymentEventType.PAYMENT_FAILED,
                    event_data={
                        "error": momo_response.get("error", "Unknown error"),
                        "momo_response": momo_response
                    }
                )
                
                return False, "Lỗi tạo thanh toán MoMo", None
            
            # Update payment với thông tin MoMo
            repository.update_payment_momo_info(
                db=db,
                payment_id=db_payment.id,
                provider_transaction_id=momo_response.get("order_id"),
                payment_info=serialize_json(momo_response.get("raw_response", {})),
                raw_response=serialize_json(momo_response)
            )
            
            response_data = {
                "payment_id": db_payment.id,
                "order_id": momo_response.get("order_id"),
                "payment_url": momo_response.get("payment_url"),
                "qr_code_url": momo_response.get("qr_code_url"),
                "message": momo_response.get("message", "Tạo thanh toán thành công")
            }
            
            logger.info(f"Created MoMo payment for payment_id {db_payment.id}")
            
            return True, "Tạo thanh toán MoMo thành công", response_data
            
        except Exception as e:
            logger.error(f"Error creating MoMo payment: {str(e)}")
            if 'db_payment' in locals():
                repository.update_payment_status(
                    db, db_payment.id, PaymentStatus.FAILED
                )
            return False, "Lỗi hệ thống", None
    
    async def handle_momo_callback(
        self,
        db: Session,
        callback_data: Dict[str, Any]
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Xử lý callback từ MoMo
        
        Args:
            db: Database session
            callback_data: Dữ liệu callback từ MoMo
            
        Returns:
            Tuple (success, message, processed_data)
        """
        try:
            # Verify callback signature
            is_valid, verify_message, processed_data = self.momo_service.verify_callback(callback_data)
            
            if not is_valid:
                logger.warning(f"Invalid MoMo callback signature: {verify_message}")
                return False, "Invalid signature", None
            
            # Tìm payment theo order_id
            order_id = processed_data.get("order_id")
            if not order_id:
                return False, "Missing order_id", None
            
            db_payment = repository.get_payment_by_provider_transaction_id(db, order_id)
            if not db_payment:
                logger.warning(f"Payment not found for order_id: {order_id}")
                return False, "Payment not found", None
            
            # Log callback event
            repository.create_payment_log(
                db=db,
                payment_id=db_payment.id,
                event_type=PaymentEventType.CALLBACK,
                event_data={
                    "provider": "momo",
                    "result_code": processed_data.get("result_code"),
                    "trans_id": processed_data.get("trans_id"),
                    "raw_callback": callback_data
                }
            )
            
            # Update payment status dựa trên result
            new_status = PaymentStatus.SUCCESS if processed_data.get("status") == "success" else PaymentStatus.FAILED
            
            repository.update_payment_status(
                db=db,
                payment_id=db_payment.id,
                status=new_status,
                provider_transaction_id=str(processed_data.get("trans_id", "")),
                raw_response=serialize_json(callback_data)
            )
            
            # Log final status
            event_type = PaymentEventType.PAYMENT_SUCCESS if new_status == PaymentStatus.SUCCESS else PaymentEventType.PAYMENT_FAILED
            
            repository.create_payment_log(
                db=db,
                payment_id=db_payment.id,
                event_type=event_type,
                event_data={
                    "final_status": new_status.value,
                    "trans_id": processed_data.get("trans_id"),
                    "amount": processed_data.get("amount"),
                    "message": processed_data.get("message")
                }
            )
            
            # TODO: Gửi notification tới Booking Service nếu thành công
            if new_status == PaymentStatus.SUCCESS:
                await self._notify_booking_service(db_payment.booking_id, "payment_success", {
                    "payment_id": db_payment.id,
                    "amount": str(db_payment.amount),
                    "trans_id": processed_data.get("trans_id")
                })
            
            logger.info(f"Processed MoMo callback for payment {db_payment.id}: {new_status.value}")
            
            return True, "Callback processed successfully", {
                "payment_id": db_payment.id,
                "booking_id": db_payment.booking_id,
                "status": new_status.value,
                "trans_id": processed_data.get("trans_id"),
                "amount": str(db_payment.amount)
            }
            
        except Exception as e:
            logger.error(f"Error handling MoMo callback: {str(e)}")
            return False, "Internal server error", None
    
    async def process_refund(
        self,
        db: Session,
        refund_request: RefundRequest
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Xử lý hoàn tiền
        
        Args:
            db: Database session
            refund_request: Dữ liệu yêu cầu hoàn tiền
            
        Returns:
            Tuple (success, message, refund_data)
        """
        try:
            # Tìm payment
            db_payment = repository.get_payment(db, str(refund_request.payment_id))
            if not db_payment:
                return False, "Payment not found", None
            
            if db_payment.status != PaymentStatus.SUCCESS:
                return False, "Chỉ có thể hoàn tiền cho giao dịch thành công", None
            
            # Tính số tiền hoàn
            refund_amount = refund_request.refund_amount or db_payment.amount
            
            if refund_amount > db_payment.amount:
                return False, "Số tiền hoàn không được lớn hơn số tiền gốc", None
            
            # Log refund request
            repository.create_payment_log(
                db=db,
                payment_id=db_payment.id,
                event_type=PaymentEventType.REFUND,
                event_data={
                    "refund_amount": str(refund_amount),
                    "reason": refund_request.reason,
                    "requested_at": datetime.utcnow().isoformat()
                }
            )
            
            # TODO: Implement actual refund logic với MoMo API
            # Hiện tại chỉ update status trong database
            
            logger.info(f"Processed refund request for payment {db_payment.id}")
            
            return True, "Yêu cầu hoàn tiền đã được ghi nhận", {
                "payment_id": db_payment.id,
                "refund_amount": str(refund_amount),
                "status": "processing",
                "message": "Yêu cầu hoàn tiền sẽ được xử lý trong 1-3 ngày làm việc"
            }
            
        except Exception as e:
            logger.error(f"Error processing refund: {str(e)}")
            return False, "Lỗi hệ thống", None
    
    async def get_payment_status(
        self,
        db: Session,
        booking_id: str
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Lấy trạng thái thanh toán theo booking_id
        
        Args:
            db: Database session
            booking_id: ID của booking
            
        Returns:
            Tuple (success, message, payment_data)
        """
        try:
            db_payment = repository.get_payment_by_booking_id(db, booking_id)
            
            if not db_payment:
                return False, "Payment not found", None
            
            payment_data = {
                "payment_id": db_payment.id,
                "booking_id": db_payment.booking_id,
                "amount": str(db_payment.amount),
                "method": db_payment.method.value,
                "status": db_payment.status.value,
                "description": db_payment.description,
                "provider_transaction_id": db_payment.provider_transaction_id,
                "transaction_time": db_payment.transaction_time.isoformat(),
                "created_at": db_payment.created_at.isoformat(),
                "updated_at": db_payment.updated_at.isoformat()
            }
            
            return True, "Success", payment_data
            
        except Exception as e:
            logger.error(f"Error getting payment status: {str(e)}")
            return False, "Lỗi hệ thống", None
    
    async def _notify_booking_service(
        self,
        booking_id: str,
        event_type: str,
        data: Dict[str, Any]
    ):
        """
        Gửi notification tới Booking Service để xác nhận booking
        
        Args:
            booking_id: ID của booking
            event_type: Loại event
            data: Dữ liệu kèm theo
        """
        try:
            import httpx
            
            if event_type == "payment_success":
                # Gọi endpoint confirm của booking service
                booking_confirm_url = f"{settings.booking_service_url}/{booking_id}/confirm"
                
                logger.info(f"Calling Booking Service to confirm booking {booking_id} at {booking_confirm_url}")
                
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.put(booking_confirm_url)
                    
                    if response.status_code == 200:
                        logger.info(f"✅ Successfully confirmed booking {booking_id} in Booking Service")
                        logger.info(f"Booking Service response: {response.json()}")
                    else:
                        logger.error(
                            f"❌ Failed to confirm booking {booking_id}. "
                            f"Status: {response.status_code}, Response: {response.text}"
                        )
            else:
                logger.info(f"Event type {event_type} does not require booking confirmation")
                
        except Exception as e:
            logger.error(f"❌ Error notifying Booking Service for booking {booking_id}: {str(e)}")
            # Không raise exception để không ảnh hưởng đến payment flow