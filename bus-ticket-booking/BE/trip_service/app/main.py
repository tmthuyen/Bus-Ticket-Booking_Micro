
from fastapi import FastAPI, Depends, HTTPException 
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from . import repository, models, schemas, utils
from .response import successResponse, errorResponse
from .database import SessionLocal, engine
# from .config import settings  
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
 

tags_metadata = [
    {
        "name": "trips",
        "description": "Operations with trips.",
    },
]
# Khởi tạo ứng dụng FastAPI với thông tin cơ bản
app = FastAPI(
    title="Trip Service",  # Tên service
    description="Service xử lý thông tin chuyến đi",  # Mô tả
    version="2.0.0",  # Phiên bản
    docs_url="/trips/docs",  # Swagger UI path
    redoc_url="/trips/redoc",  # ReDoc path
    openapi_tags=tags_metadata,  # Thêm thẻ (tags) cho OpenAPI
)

app.add_middleware( # cau hinh CORS
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn (có thể thay đổi để chỉ cho phép một số nguồn cụ thể)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các tiêu đề
)

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

# API endpoints sẽ được định nghĩa ở đây
@app.get("/health", tags=["trips"])
def health_check():
    """Kiểm tra trạng thái  hoạt động của dịch vụ chuyến đi."""
    return {"status": "Trip Service is healthy"}


@app.get("/routes", response_model=successResponse, tags=["routes"])
def get_routes(db: Session = Depends(get_db), origin_code: str = '', destination_code: str = '', limit: int = 100, offset: int = 0):
    """Lấy danh sách tất cả các chuyến đi."""
    routes = repository.get_routes(db=db, origin_code=origin_code, destination_code=destination_code, limit=limit, offset=offset)
    routesResponse = [schemas.RouteResponse.model_validate(route) for route in routes]
    return successResponse(
        msg="Routes retrieved successfully", 
        data=jsonable_encoder(routesResponse)
    )

# /trips?origin_code=&destination_code=&from_date=&limit=&offset=
@app.get("/trips-by-route", response_model=successResponse, tags=["trips"])
def get_trips(
    origin_code: str, 
    destination_code: str, 
    from_date: str, 
    limit: int = 100, 
    offset: int = 0, 
    db: Session = Depends(get_db)):
    """Lấy danh sách tất cả các chuyến đi."""
    # Kiem tra du lieu dau vao
    if not origin_code or not destination_code or not from_date:
        return errorResponse(msg="origin_code, destination_code, and from_date are required parameters.")
    
    # lay tu repository
    trips, total = repository.get_trips_by_origin_destination_and_date(
        db=db, 
        origin_code=origin_code, 
        destination_code=destination_code, 
        from_date=from_date, 
        limit=limit, offset=offset
    )
    return successResponse(
        msg="Trips retrieved successfully", 
        data=jsonable_encoder(trips)
    )

# trips/{trip_id}
@app.get("/trips/{trip_id}", response_model=successResponse, tags=["trips"])
def get_trip_by_id(
    trip_id: int,  
    db: Session = Depends(get_db)):
    """Lấy thông tin chuyến đi theo ID."""
    if not trip_id:
        return errorResponse(msg="Thiếu trip_id.")
    
    trip = repository.get_trip_by_id(db=db, trip_id=trip_id)
    if not trip:
        return errorResponse(msg="Trip not found.", status_code=404)
    
    return successResponse(msg="Trip retrieved successfully", data=jsonable_encoder(trip))

@app.put("/trips/{trip_id}", response_model=successResponse, tags=["trips"])
def update_trip(
    trip_id: int, 
    trip_data: schemas.Trip, 
    db: Session = Depends(get_db)):
    """Cập nhật thông tin chuyến đi theo ID."""
    if not trip_id:
        return errorResponse(msg="Thiếu trip_id.")
    if not trip_data:
        return errorResponse(msg="Thiếu dữ liệu cập nhật chuyến đi.")
    if trip_data.status not in [schemas.TripStatus.SCHEDULED.value, schemas.TripStatus.BOARDING.value,
                                 schemas.TripStatus.DEPARTED.value, schemas.TripStatus.CANCELLED.value, 
                                 schemas.TripStatus.COMPLETED.value]:
        return errorResponse(msg=f"Trạng thái chuyến đi không hợp lệ.")

    updated_trip = repository.update_trip(db=db, trip_id=trip_id, trip_data=trip_data)
    return successResponse(msg="Trip updated successfully", data=updated_trip)

# /seats?trip_id=
@app.get("/seats-by-trip/{trip_id}", response_model=successResponse, tags=["seats"])
def get_seats_by_trip_id(
    trip_id: int,  
    db: Session = Depends(get_db)):
    """Lấy danh sách ghế theo ID chuyến đi và danh sách ghế cụ thể.""" 
    seats = repository.get_seat_layout_by_trip_id(db=db, trip_id=trip_id)
    return successResponse(msg="Seats retrieved successfully", data=seats)

 
@app.get("/payment-test/callback", tags=["payment-test"])
def payment_callback(partnerCode: str, orderId: str, amount: float, orderInfo: str, orderType: str, transId: int, resultCode: int, message: str, payType: int, responseTime: str, extraData: str, signature: str):
    """Endpoint test callback từ payment service. Cho momo, vnpay,..."""
    print("Callback received:")
    print(f"partnerCode: {partnerCode}")
    print(f"orderId: {orderId}")
    print(f"amount: {amount}")
    print(f"orderInfo: {orderInfo}")
    print(f"orderType: {orderType}")
    print(f"transId: {transId}")
    return {
        "partnerCode": partnerCode,
        "orderId": orderId,
        "errorCode": errorCode
    }
    
