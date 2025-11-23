
from fastapi import FastAPI, Depends, HTTPException, Request 
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from . import repository, models, schemas, utils, helper_apis
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
async def get_seats_by_trip_id(
    trip_id: int,  
    db: Session = Depends(get_db)
):
    """Lấy danh sách ghế theo ID chuyến đi và danh sách ghế cụ thể.""" 
    seats = repository.get_seat_layout_by_trip_id(db=db, trip_id=trip_id)
    
    try:
        success, seats_data = await helper_apis.get_booked_seats_by_trip_id_in_booking_service(trip_id)
        if not success:
            return errorResponse(
                status_code=400,
                msg=seats_data.get("detail", "Error fetching trip information")
            ) 
    except Exception as e:
        return errorResponse(
            status_code=500,
            msg=str(e)
        )
    
    # "trip_id": 3,
    # "booked_seat_numbers": [],
    # "total_booked": 0
    
    booked_seat_numbers = seats_data.get("booked_seat_numbers", []) if seats_data else []
    
    for seat in seats:
        if seat.get("seat_number", None) in booked_seat_numbers:
            seat["is_booked"] = True
        else:
            seat["is_booked"] = False
            
    response_data = {
        "trip_id": trip_id,
        "seat_layout": seats,
        "total_seats": len(seats),
        "total_booked": len(set(booked_seat_numbers)),
    }
    
    
    
    return successResponse(msg="Seats retrieved successfully", data=response_data)

 

    
