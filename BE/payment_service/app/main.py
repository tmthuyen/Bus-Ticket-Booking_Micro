from decimal import Decimal
from typing import Dict, Any
import logging
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db
from .config import settings
from .response import successResponse, errorResponse
from .services.payment_service import PaymentService
from .services.momo_service import MoMoService
from .utils import serialize_json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Tạo các bảng trong database nếu chưa tồn tại
models.Base.metadata.create_all(bind=engine)

# Metadata cho OpenAPI docs
tags_metadata = [
    {
        "name": "payments",
        "description": "Core payment operations",
    },
    {
        "name": "momo",
        "description": "MoMo payment gateway integration",
    },
    {
        "name": "health",
        "description": "Health check and monitoring",
    }
]

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title=settings.service_name,
    description="Service xử lý thanh toán đặt vé xe với tích hợp MoMo",
    version=settings.service_version,
    docs_url="/payments/docs",
    redoc_url="/payments/redoc",
    openapi_tags=tags_metadata,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: thay bằng domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Production: thay bằng hosts cụ thể
)

# Initialize services
payment_service = PaymentService()
momo_service = MoMoService()

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return errorResponse(
        status_code=exc.status_code,
        msg=exc.detail
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return errorResponse(
        status_code=500,
        msg="Internal server error"
    )

# ===== HEALTH CHECK ENDPOINTS =====

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return successResponse(
        msg="Service is healthy",
        data={
            "service": settings.service_name,
            "version": settings.service_version,
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.get("/health/db", tags=["health"])
async def health_check_db(db: Session = Depends(get_db)):
    """Database health check"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return successResponse(
            msg="Database is healthy",
            data={
                "database": "ok",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return errorResponse(
            status_code=503,
            msg="Database is unhealthy"
        )

# ===== CORE PAYMENT ENDPOINTS =====
@app.post("/payments", tags=["payments"])
async def create_payment(
    payment: schemas.PaymentCreate, 
    db: Session = Depends(get_db)
):
    """Tạo một payment mới với proper JSON response"""
    try:
        success, message, db_payment = await payment_service.create_payment(db, payment)
        
        if not success:
            return errorResponse(status_code=400, msg=message)
        
        # ✅ FIXED: Convert SQLAlchemy object to dict
        return successResponse(
            msg="Payment created successfully",
            data=db_payment.to_dict()  # Use model's to_dict method
        )
        
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        return errorResponse(status_code=500, msg="Internal server error")

@app.get("/payments/{payment_id}", response_model=schemas.PaymentOut, tags=["payments"])
async def get_payment(payment_id: str, db: Session = Depends(get_db)):
    """Lấy thông tin payment theo ID"""
    from . import repository
    
    db_payment = repository.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        return errorResponse(status_code=404, msg="Payment not found")
    
    payment_dict = {
        "id": db_payment.id,
        "booking_id": db_payment.booking_id,
        "amount": str(db_payment.amount),  
        "method": db_payment.method.value,  
        "status": db_payment.status.value,  
        "description": db_payment.description,
        "provider_transaction_id": db_payment.provider_transaction_id,
        "transaction_time": db_payment.transaction_time.isoformat(),
        "created_at": db_payment.created_at.isoformat() if hasattr(db_payment, 'created_at') and db_payment.created_at else None,
        "updated_at": db_payment.updated_at.isoformat() if hasattr(db_payment, 'updated_at') and db_payment.updated_at else None
    }
    
    return successResponse(
        msg="Payment found",
        data=payment_dict
    )

@app.get("/payments/status/{booking_id}", tags=["payments"])
async def get_payment_status(booking_id: str, db: Session = Depends(get_db)):
    """Lấy trạng thái thanh toán theo booking ID"""
    try:
        success, message, payment_data = await payment_service.get_payment_status(db, booking_id)
        
        if not success:
            return errorResponse(status_code=404, msg=message)
        
        return successResponse(
            msg="Payment status retrieved",
            data=payment_data
        )
        
    except Exception as e:
        logger.error(f"Error getting payment status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ===== MOMO PAYMENT ENDPOINTS =====

@app.post("/payments/momo/create", tags=["momo"])
async def create_momo_payment(
    payment_request: schemas.MoMoPaymentRequest,
    db: Session = Depends(get_db)
):
    """Tạo thanh toán MoMo"""
    try:
        success, message, response_data = await payment_service.create_momo_payment(
            db, payment_request
        )
        
        if not success:
            return errorResponse(status_code=400, msg=message)
        
        return successResponse(
            msg="MoMo payment created successfully",
            data=response_data
        )
        
    except Exception as e:
        logger.error(f"Error creating MoMo payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/payments/momo/callback", tags=["momo"])
async def momo_callback(
    callback_data: schemas.MoMoCallbackRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Nhận callback từ MoMo"""
    try:
        # Convert Pydantic model to dict
        callback_dict = callback_data.dict()
        
        success, message, processed_data = await payment_service.handle_momo_callback(
            db, callback_dict
        )
        
        if not success:
            logger.warning(f"MoMo callback processing failed: {message}")
            return errorResponse(status_code=400, msg=message)
        
        # MoMo yêu cầu response format cụ thể
        return JSONResponse(
            status_code=200,
            content={
                "payment_id": processed_data.get("payment_id"),
                "booking_id": processed_data.get("booking_id"),
                "partnerCode": callback_data.partnerCode,
                "orderId": callback_data.orderId,
                "requestId": callback_data.requestId,
                "resultCode": 0,  # 0 = success
                "message": "success",
                "responseTime": int(datetime.utcnow().timestamp() * 1000)
            }
        )
        
    except Exception as e:
        logger.error(f"Error handling MoMo callback: {str(e)}")
        # Vẫn trả success cho MoMo để tránh retry
        return JSONResponse(
            status_code=200,
            content={
                "partnerCode": callback_data.partnerCode,
                "orderId": callback_data.orderId,
                "requestId": callback_data.requestId,
                "resultCode": 1,  # 1 = failed
                "message": "processing error",
                "responseTime": int(datetime.utcnow().timestamp() * 1000)
            }
        )
# app/main.py - THÊM ENDPOINT NÀY
@app.post("/payments/sync-momo-status/{booking_id}", tags=["momo"])
async def sync_momo_payment_status(booking_id: str, db: Session = Depends(get_db)):
    """Sync payment status với MoMo khi callback bị lỗi"""
    try:
        from . import repository
        
        # Tìm payment theo booking_id
        db_payment = repository.get_payment_by_booking_id(db, booking_id)
        
        if not db_payment:
            return errorResponse(status_code=404, msg="Payment not found")
        
        if db_payment.status == models.PaymentStatus.SUCCESS:
            return successResponse(
                msg="Payment already successful", 
                data={"status": "SUCCESS", "booking_id": booking_id}
            )
        
        # Get order_id from provider_transaction_id
        order_id = db_payment.provider_transaction_id
        
        if not order_id:
            return errorResponse(status_code=400, msg="No order_id found")
        
        logger.info(f"🔄 Syncing payment status for booking {booking_id}, order_id: {order_id}")
        
        # Query MoMo status
        momo_result = momo_service.query_transaction_status(order_id, "sync-request")
        
        if momo_result.get("success") and momo_result.get("result_code") == 0:
            # Update to SUCCESS
            repository.update_payment_status(
                db,
                db_payment.id,
                models.PaymentStatus.SUCCESS,
                provider_transaction_id=str(momo_result.get("trans_id", "")),
                raw_response=serialize_json(momo_result)
            )
            
            # Log success event
            repository.create_payment_log(
                db=db,
                payment_id=db_payment.id,
                event_type=models.PaymentEventType.PAYMENT_SUCCESS,
                event_data={
                    "source": "manual_sync",
                    "momo_result": momo_result,
                    "sync_time": datetime.utcnow().isoformat()
                }
            )
            
            logger.info(f"✅ Synced payment {db_payment.id} to SUCCESS")
            
            # Gọi Booking Service để xác nhận booking
            await payment_service._notify_booking_service(
                booking_id=booking_id,
                event_type="payment_success",
                data={
                    "payment_id": db_payment.id,
                    "amount": str(db_payment.amount),
                    "trans_id": momo_result.get("trans_id")
                }
            )
            
            return successResponse(
                msg="Payment status synced successfully",
                data={
                    "payment_id": db_payment.id,
                    "booking_id": booking_id,
                    "old_status": "PENDING",
                    "new_status": "SUCCESS",
                    "momo_trans_id": momo_result.get("trans_id")
                }
            )
        else:
            return successResponse(
                msg="MoMo payment not successful yet",
                data={
                    "status": db_payment.status.value,
                    "momo_result_code": momo_result.get("result_code"),
                    "momo_message": momo_result.get("message")
                }
            )
            
    except Exception as e:
        logger.error(f"💥 Error syncing payment status: {str(e)}")
        return errorResponse(status_code=500, msg="Sync failed")

# ===== REFUND ENDPOINTS =====

@app.post("/payments/{payment_id}/refund", tags=["payments"])
async def refund_payment(
    payment_id: str,
    refund_request: schemas.RefundRequest,
    db: Session = Depends(get_db)
):
    """Yêu cầu hoàn tiền"""
    try:
        # Override payment_id từ URL
        refund_request.payment_id = payment_id
        
        success, message, refund_data = await payment_service.process_refund(
            db, refund_request
        )
        
        if not success:
            return errorResponse(status_code=400, msg=message)
        
        return successResponse(
            msg="Refund request processed",
            data=refund_data
        )
        
    except Exception as e:
        logger.error(f"Error processing refund: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ===== ADMIN/DEBUG ENDPOINTS =====

@app.get("/payments/{payment_id}/logs", tags=["payments"])
async def get_payment_logs(payment_id: str, db: Session = Depends(get_db)):
    """Lấy logs của payment (for debugging)"""
    from . import repository
    
    logs = repository.get_payment_logs(db, payment_id)
    
    return successResponse(
        msg="Payment logs retrieved",
        data=[{
            "id": log.id,
            "event_type": log.event_type.value,
            "event_data": log.event_data,
            "created_at": log.created_at.isoformat()
        } for log in logs]
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return successResponse(
        msg="Payment Service API",
        data={
            "service": settings.service_name,
            "version": settings.service_version,
            "docs": "/payments/docs",
            "health": "/health"
        }
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)