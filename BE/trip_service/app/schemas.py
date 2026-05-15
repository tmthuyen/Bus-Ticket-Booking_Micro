from pydantic import BaseModel, ConfigDict, computed_field
from typing import Optional
from datetime import datetime 
from enum import Enum
from . import models

 

class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int 
    origin: Optional[str] = None
    origin_code: Optional[str] = None
    destination: Optional[str] = None 
    destination_code: Optional[str] = None
    base_price: Optional[float] = 0.0
    distance_km: Optional[float] = 0.0
    estimated_duration: Optional[int] = 0  # in minutes
    @computed_field
    @property
    def estimated_duration_hour(self) -> float:
        format_decimal = 2
        return round((self.estimated_duration or 0) / 60.0, format_decimal)
    status: Optional[models.BaseStatus] = models.BaseStatus.ACTIVE.value
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # class Config:
    #     from_attributes = True

class BusModelResponse(BaseModel):
    id: int
    name: Optional[str] = None
    deck_count: Optional[int] = None
    total_seats: Optional[int] = None
    status: Optional[models.BaseStatus] = models.BaseStatus.ACTIVE.value
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
         
class SeatTemplateResponse(BaseModel):
    id: int
    bus_model_id: int
    seat_number: Optional[str] = None
    floor: Optional[int] = None
    row_index: Optional[int] = None
    col_index: Optional[int] = None 
    
    class Config:
        from_attributes = True
        
class BusResponse(BaseModel):
    id: int
    bus_model_id: int
    plate_number: Optional[str] = None
    status: Optional[models.BusStatus] = models.BusStatus.ACTIVE.value
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Trip(BaseModel):
    id: int
    route_id: Optional[int] = None
    bus_id: Optional[int] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None 
    total_seats: Optional[int] = None 
    status: Optional[models.TripStatus] = models.TripStatus.SCHEDULED.value
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None    
    
    class Config:
        from_attributes = True
 
 