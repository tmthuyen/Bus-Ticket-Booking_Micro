from sqlalchemy.orm import Session
from . import models, schemas, utils
import datetime 

# ========= ROUTES =========
#  get routes
def get_routes(db: Session, origin_code: str = '', destination_code: str = '', limit: int = 100, offset: int = 0):
    """Lấy danh sách tất cả các tuyến đường với tùy chọn lọc theo điểm xuất phát và điểm đến."""
    query = db.query(models.Route)
    if origin_code:
        query = query.filter(models.Route.origin_code.ilike(f"%{origin_code}%"))
    if destination_code:
        query = query.filter(models.Route.destination_code.ilike(f"%{destination_code}%"))
    routes = query.offset(offset).limit(limit).all()
    return routes
  
# ========= TRIPS =========
def get_trips_by_origin_destination_and_date(db: Session, origin_code: str, destination_code: str, from_date: str, limit: int = 100, offset: int = 0):
    """Lấy danh sách các chuyến đi dựa trên điểm xuất phát và điểm đến."""
    origin_code = f"{origin_code.strip().lower()}%"
    destination_code = f"{destination_code.strip().lower()}%"
    start_utc, end_utc = utils.local_date_to_utc_range(from_date)
    
    base = (
        db.query(models.Trip, models.Route, models.Bus)
        .join(models.Route, models.Trip.route_id == models.Route.id)
        .join(models.Bus, models.Trip.bus_id == models.Bus.id)
        .filter(
            models.Route.origin_code.ilike(origin_code),
            models.Route.destination_code.ilike(destination_code),
            models.Trip.departure_time >= start_utc,
            models.Trip.departure_time < end_utc,
        )
        .order_by(models.Trip.departure_time.asc())
    )
    
    total = base.count()
    rows = base.offset(offset).limit(limit).all()
    trips = []
    for trip, route, bus in rows:
        data = {
            "id": trip.id,
            "route_id": trip.route_id,
            "bus_id": trip.bus_id,
            "departure_time": trip.departure_time.isoformat(), # trả về thời gian UTC iso format
            "arrival_time": trip.arrival_time.isoformat(),
            "created_at": trip.created_at.isoformat(),
            "updated_at": trip.updated_at.isoformat(),
            "status": trip.status,
            "plate_number": bus.plate_number,
            "origin": route.origin,
            "origin_code": route.origin_code,
            "destination": route.destination,
            "destination_code": route.destination_code,
            "distance_km": route.distance_km,
            "estimated_duration": route.estimated_duration,
            "estimated_duration_hour": route.estimated_duration / 60.0,
            "base_price": route.base_price,
            "total_seats": bus.bus_model.total_seats,
            # "bus_model": bus.bus_model,
            # "route": trip.route,
            "bus": trip.bus,
        }
        trips.append(data)
    
    return trips, total
 

def update_trip(db: Session, trip_id: int, trip_data: schemas.Trip):
    """Cập nhật thông tin chuyến đi theo ID."""
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        return None
    
    if trip_data.departure_time is not None:
        trip.departure_time = trip_data.departure_time
    if trip_data.arrival_time is not None:
        trip.arrival_time = trip_data.arrival_time
    if trip_data.status is not None:
        trip.status = trip_data.status 
        
    db.commit()
    db.refresh(trip)
    return trip

def get_trip_by_id(db: Session, trip_id: int):
    """Lấy thông tin chuyến đi theo ID."""
    base = (
        db.query(models.Trip, models.Route)
        .join(models.Route, models.Trip.route_id == models.Route.id)
        .filter(models.Trip.id == trip_id)
    )
    
    row = base.first()
    if not row:
        return None
    trip, route = row
    trip_data = {
        "id": trip.id,
        "route_id": trip.route_id,
        "bus_id": trip.bus_id,
        "departure_time": trip.departure_time.isoformat(), # trả về thời gian UTC iso format
        "arrival_time": trip.arrival_time.isoformat(),
        "created_at": trip.created_at.isoformat(),
        "updated_at": trip.updated_at.isoformat(),
        "status": trip.status,
        "route": {
            "id": route.id,
            "origin": route.origin,
            "origin_code": route.origin_code,
            "destination": route.destination,
            "destination_code": route.destination_code,
            "base_price": route.base_price,
            "distance_km": route.distance_km,
            "estimated_duration": route.estimated_duration,
        }, 
        "bus": trip.bus,
    }
    return trip_data

# ========= SEATS =========    
def get_seat_layout_by_trip_id(db: Session, trip_id: int):
    """Lấy sơ đồ chỗ ngồi cho chuyến đi dựa trên trip_id."""
    base = (
        db.query(models.Trip, models.Bus, models.SeatTemplate)
        .join(models.Bus, models.Trip.bus_id == models.Bus.id)
        .join(models.SeatTemplate, models.Bus.bus_model_id == models.SeatTemplate.bus_model_id)
        .filter(models.Trip.id == trip_id)
        .order_by(
            models.SeatTemplate.floor.asc(), 
            models.SeatTemplate.seat_number.asc()
        )
    )
    
    rows = base.all()
    seat_layout = []
    for trip, bus, seat_template in rows:
        seat_info = {
            "seat_id": seat_template.id,
            "seat_number": seat_template.seat_number,
            "floor": seat_template.floor,
            "row_index": seat_template.row_index,
            "col_index": seat_template.col_index,
        }
        seat_layout.append(seat_info)
    
    return seat_layout