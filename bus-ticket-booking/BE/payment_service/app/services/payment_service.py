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
        self.payment_expiry_minutes = 15;  # Thời gian hết hạn payment
    
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
            existing_payment = self._get_valid_pending_payment(db, str(payment_request.booking_id)) # Kiểm tra payment pending hợp lệ
            if existing_payment:
                logger.info(f"Found existing pending payment for booking {payment_request.booking_id}")
                return self._return_existing_payment(existing_payment)
            
            expired_count = repository.expire_old_pending_payments(db, str(payment_request.booking_id)) # Expire các payment pending cũ
            if expired_count > 0:
                logger.info(f"Expired {expired_count} old pending payments for booking {payment_request.booking_id}")
                
            logger.info(f"Creating new MoMo payment for booking {payment_request.booking_id}")

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
                booking_confirm_url = f"{settings.booking_service_url}/bookings/{booking_id}/confirm"
                
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


    def _get_valid_pending_payment(self, db: Session, booking_id: str) -> Optional[Payment]:
        """Lấy pending payment hợp lệ (chưa expire)"""
        pending_payment = repository.get_pending_payment_by_booking(db, booking_id)
        
        if not pending_payment:
            return None
            
        if self._is_payment_expired(pending_payment):
            logger.info(f"⏰ Payment {pending_payment.id} has expired")
            return None
            
        return pending_payment

    def _is_payment_expired(self, payment: Payment) -> bool:
        """Kiểm tra payment đã expire chưa"""
        if not payment.created_at:
            return True
            
        from datetime import timedelta
        expiry_time = payment.created_at + timedelta(minutes=self.payment_expiry_minutes)
        return datetime.utcnow() > expiry_time

    def _return_existing_payment(self, payment: Payment) -> Tuple[bool, str, Dict[str, Any]]:
        """Trả về thông tin payment existing"""
        try:
            from datetime import timedelta
            import json
            
            # Tính thời gian còn lại
            expiry_time = payment.created_at + timedelta(minutes=self.payment_expiry_minutes)
            time_remaining = int((expiry_time - datetime.utcnow()).total_seconds())
            
            # Parse raw_response để lấy URLs
            payment_url = ""
            qr_code_url = ""
            
            if payment.raw_response:
                try:
                    parsed = json.loads(payment.raw_response)
                    logger.info(f"🔍 DEBUG: Full raw_response structure: {json.dumps(parsed, indent=2)}")
                    
                    # ✅ FIX: Check multiple locations for URLs
                    
                    # Location 1: Direct fields (from momo_service response)
                    payment_url = parsed.get('payment_url', '')
                    qr_code_url = parsed.get('qr_code_url', '')
                    
                    # Location 2: In nested raw_response (from MoMo API)
                    if not payment_url and 'raw_response' in parsed:
                        inner_response = parsed['raw_response']
                        if isinstance(inner_response, dict):
                            payment_url = inner_response.get('payUrl', '')
                            qr_code_url = inner_response.get('qrCodeUrl', '')
                    
                    # Location 3: Direct MoMo fields (fallback)
                    if not payment_url:
                        payment_url = parsed.get('payUrl', '')
                        qr_code_url = parsed.get('qrCodeUrl', '')
                        
                    logger.info(f"🔍 Extracted URLs: payment_url='{payment_url}', qr_code_url='{qr_code_url}'")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse raw_response: {str(e)}")
            
            # ✅ FALLBACK: Check payment_info column
            if not payment_url and payment.payment_info:
                try:
                    payment_info = json.loads(payment.payment_info)
                    logger.info(f"🔍 DEBUG: payment_info structure: {json.dumps(payment_info, indent=2)}")
                    
                    payment_url = payment_info.get('payUrl', '')
                    qr_code_url = payment_info.get('qrCodeUrl', '')
                    
                    logger.info(f"🔍 From payment_info: payment_url='{payment_url}', qr_code_url='{qr_code_url}'")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse payment_info: {str(e)}")
            
            # ✅ VALIDATION: Ensure URLs are valid
            if not payment_url or not payment_url.startswith('http'):
                logger.warning(f"⚠️ Invalid payment_url found: '{payment_url}'")
                payment_url = f"https://test-payment.momo.vn/v2/gateway/pay?orderId={payment.provider_transaction_id}"
            
            response_data = {
                "payment_id": payment.id,
                "order_id": payment.provider_transaction_id,
                "payment_url": payment_url,
                "qr_code_url": qr_code_url,
                "is_existing": True,
                "expires_at": expiry_time.isoformat() + "Z",
                "time_remaining_seconds": max(0, time_remaining),
                "amount": str(payment.amount),
                "message": "Tiếp tục thanh toán hiện có"
            }
            
            logger.info(f"✅ Returning existing payment with URLs: payment_url='{payment_url[:50]}...', qr_code_url='{qr_code_url[:50] if qr_code_url else ''}'")
            
            return True, "Payment continued successfully", response_data
            
        except Exception as e:
            logger.error(f"Error returning existing payment: {str(e)}")
            return False, "Lỗi trả về payment existing", None