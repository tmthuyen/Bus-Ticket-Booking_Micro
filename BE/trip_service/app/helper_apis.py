import httpx
from .config import settings

async def get_booked_seats_by_trip_id_in_booking_service(trip_id: int):
  """Gọi sang Booking Service để lấy thông tin danh sách ghế đã được đặt cho chuyến đi cụ thể."""
  async with httpx.AsyncClient() as client:
      response = await client.get(f"{settings.booking_service_url}/trip/{trip_id}/booked-seats")
     
  if response.status_code != 200:
      return False, {"detail": "Error fetching trip from Booking Service"}
    
  print("Response from Booking Service:", response.json())

  return response.status_code == 200, response.json().get("data", [])  # Trả về kết quả