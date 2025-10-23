from decimal import Decimal
from fastapi import FastAPI, Depends, HTTPException, Request  
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from . import repository, models, schemas, utils
from .database import SessionLocal, engine
from .config import settings
from .response import successResponse, errorResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware

# Tạo các bảng trong database nếu chưa tồn tại
models.Base.metadata.create_all(bind=engine)
tags_metadata = [
    {
        "name": "payments",
        "description": "Operations with payments.",
    },
]
# Khởi tạo ứng dụng FastAPI với thông tin cơ bản
app = FastAPI(
    title="Payment Service",  # Tên service
    description="Service xử lý thanh toán đặt vé xe",  # Mô tả
    version="2.0.0",  # Phiên bản
    docs_url="/payments/docs",  # Swagger UI path
    redoc_url="/payments/redoc",  # ReDoc path
    openapi_tags=tags_metadata,  # Thêm thẻ (tags) cho OpenAPI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn (cẩn thận với việc này trong môi trường production)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các headers
)

# DEPENDENCY INJECTION

def get_db():
    """Tạo và quản lý database session cho mỗi request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HELPER FUNCTIONS - CÁC HÀM HỖ TRỢ


async def generate_otp_code(payer_id: str, payment_id: str, email: str) -> bool:
    """Gọi Notify Service để tạo mã OTP"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.notify_service_url}/generateOTP/{payer_id}", json={
            "username": payer_id,
            "email": email,
            "payment_id": payment_id,
            "purpose": "PAYMENT",
        })

    return response.status_code == 200, response.json()  # Trả về kết quả

async def verify_otp_code(payer_id: str, payment_id: str, code: str, email: str) -> bool:
    """Gọi Notify Service để xác thực mã OTP"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.notify_service_url}/verifyOTP", json={
            "username": payer_id,
            "payment_id": payment_id,
            "code": code,
            "email": email
        })
        
        result = response.json()
        if response.status_code == 200:
            return True,result.get("message", "OTP hợp lệ")
    return False, result.get("message", "OTP không hợp lệ")
 
async def send_success_notification(payment_id: str, payment_info: dict):
    """Gửi thông báo thanh toán thành công qua notify_service"""
    try: 
        # Gửi yêu cầu thông báo thành công qua notify service
        async with httpx.AsyncClient(timeout=5.0) as client:
            data = {
                "payment_id": payment_id,
                "payer_id": payment_info.get("payer_id"),
                "payer_name": payment_info.get("payer_name"),
                "student_id": payment_info.get("student_id"),
                "full_name": payment_info.get("full_name"),
                "term": payment_info.get("term"),
                "amount": payment_info.get("amount"),
                "payment_status": payment_info.get("payment_status"),
                "created_at": payment_info.get("created_at"),
                "updated_at": payment_info.get("updated_at"),
                "email": payment_info.get("payer_email"),
            }
                # "payment_info": payment_info
            response = await client.post(f"{settings.notify_service_url}/paymentNotification", json=data)
            return response.status_code == 200
    except Exception as e:
        print(f"Gửi thông báo thành công thất bại: {e}")
        return False

# API ENDPOINTS

@app.get("/payments/health", tags=["payments"])
def read_root():
    return successResponse(
        msg="Payment service đang hoạt động bình thường",
        data={
            "service": "Payment Service",
            "version": "2.0.0",
            "description": "Service xử lý thanh toán học phí"
        }
    )
    
@app.post("/intent", tags=["payments"])
async def create_payment_intent(
    payment_intent: schemas.PaymentIntent,
    request: Request,
    db: Session = Depends(get_db)
):
    return successResponse(
        status_code=201,
        msg="Tạo payment intent thành công",
        data={
            "payment_id": 1,
            "amount": 500000,
            "status": "INTENDED"
        }
    )

@app.post("/{payment_id}/process", tags=["payments"])
async def process_payment(
    payment_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Xử lý thanh toán sau khi co thong tin OTP can xac thuc"""
    
    
    # Nếu thành công gửi Email thông báo bằng bất đồng bộ  
    
    return successResponse(
        msg="Thanh toán thành công",
        data={
            "payment_id": payment_id,
            "status": "COMPLETED"
        }
    )
@app.get("/{payment_id}/detail", tags=["payments"])
def get_payment_detailed_history(payment_id: str, db: Session = Depends(get_db)):
    # Lấy thông tin payment
    
    return successResponse(
        msg="Lấy thông tin payment thành công",
        data={
            "payment_id": payment_id,
            "student_id": "S123456",
            "student_name": "Nguyen Van A",
            "payer_id": 1,
            "payer_name": "Nguyen Thi B",
            "term": "2024 Spring",
            "amount": "500000.00",
            "status": "COMPLETED",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:05:00Z",
            "transactions": [
                {
                    "transaction_id": 1,
                    "transaction_type": "DEBIT",
                    "amount": "500000.00",
                    "balance_before": "1000000.00",
                    "balance_after": "500000.00",
                    "description": "Thanh toán học phí kỳ 2024 Spring",
                    "created_at": "2024-01-15T10:05:00Z"
                }
            ]
        }
    )
 
@app.get("/user/{payer_id}", tags=["payments"])
def get_payments_by_user(
    payer_id: int, 
    skip: int = 0, #cho phép phân trang
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Lấy danh sách tất cả payments của một user"""
    payments = repository.get_payments_by_payer(db, payer_id, skip, limit)
    
    return successResponse(
        msg=f"Lấy danh sách {len(payments)} payments thành công",
        data=[{
            "payment_id": p.id,
            "student_id": p.student_id,
            "student_name": p.student_name,
            "term": p.term,
            "amount": str(p.amount),
            "status": p.status.value,
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat()
        } for p in payments]
    )

    

@app.get("/transactions/{payer_id}", tags=["payments"])
def get_user_transaction_history(
    payer_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Lấy lịch sử giao dịch của user"""
    transactions = [{
        "id": 1,
        "payment_id": "pay_123456",
        "transaction_type": 'DEBIT',  # DEBIT/CREDIT
        "amount": 100000,
        "balance_before": 1000000,
        "balance_after": 900000,
        "description": "Thanh toán vé xe",
        "created_at": datetime.now()
    }]
    
    return successResponse(
        msg=f"Lấy lịch sử giao dịch thành công",
        data=[{
            "transaction_id": t.id,
            "payment_id": t.payment_id,
            "transaction_type": t.transaction_type,  # DEBIT/CREDIT
            "amount": t.amount,
            "balance_before": t.balance_before,
            "balance_after": t.balance_after,
            "description": t.description,
            "created_at": t.created_at.isoformat()
        } for t in transactions]
    )

# Thuyên all lấy dữ liệu payment
@app.get("/all", tags=["payments"])
def get_all_payments(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    payments = repository.get_all_payments(db, skip=skip, limit=limit)
    return successResponse(msg="Lấy danh sách payment thành công",
                                     data=jsonable_encoder([schemas.PaymentResponse.model_validate(t).model_dump() for t in payments])
                                        )
    