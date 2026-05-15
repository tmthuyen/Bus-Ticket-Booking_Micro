
import httpx
from .config import settings

async def get_trip_by_id_of_trip_service(trip_id: int):
  """Gọi sang Trip Service để lấy thông tin chuyến đi theo ID"""
  async with httpx.AsyncClient() as client:
      response = await client.get(f"{settings.trip_service_url}/trips/{trip_id}")
    
  if response.status_code == 400:
      return False, {"detail": "Bad request to Trip Service"}
  elif response.status_code == 404:
      return False, {"detail": "Trip not found"}
  elif response.status_code != 200:
      return False, {"detail": "Error fetching trip from Trip Service"}
  print("Response from Trip Service:", response.json())

  return response.status_code == 200, response.json()  # Trả về kết quả

async def send_otp(
    email: str,
    booking_code: str
) -> tuple[bool, dict]:
    """Gọi sang Notification Service để gửi OTP xác thực email"""
    payload = {
        "email": email,
        "booking_code": booking_code
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.notify_service_url}/otp/send", json=payload)
    
    if response.status_code == 201:
        return True, response.json()
    else:
        return False, response.json()
    
async def verify_otp(
    email: str,
    otp_code: str
) -> tuple[bool, dict]:
    """Gọi sang Notification Service để xác thực OTP"""
    payload = {
        "email": email,
        "otp": otp_code
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.notify_service_url}/otp/verify", json=payload)
    
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json()