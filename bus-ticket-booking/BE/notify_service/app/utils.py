from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone
import smtplib
import ssl
import logging
import random
import string

logger = logging.getLogger(__name__)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "minhtuank27tdtu@gmail.com"
SENDER_PASSWORD = "scxwnfestbszztcf"

def send_email(receiver_email: str, subject: str, body: str, is_html: bool = False) -> bool:
    """
    Gửi email chung
    """
    try:
        if is_html:
            msg = MIMEMultipart("alternative")
            msg.attach(MIMEText(body, "html"))
        else:
            msg = MIMEText(body, "plain")
        
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ssl.create_default_context()) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        
        logger.info(f"Email sent successfully to {receiver_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {receiver_email}: {str(e)}")
        return False

def send_booking_confirmation_email(
    receiver_email: str,
    booking_code: str,
    customer_name: str,
    trip_info: str,
    seat_numbers: list[str],
    total_price: float,
    booking_time: str
) -> bool:
    subject = f"Xác nhận đặt vé - Mã đặt chỗ: {booking_code}"
    
    # Format danh sách ghế
    seats_display = ", ".join(seat_numbers)  # "A1, A2, B5"
    seat_count = len(seat_numbers)
    
    body = f"""
Kính gửi {customer_name},

Cảm ơn bạn đã đặt vé xe khách của chúng tôi!

THÔNG TIN ĐẶT VÉ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mã đặt chỗ: {booking_code}
Thời gian đặt: {booking_time}
Chuyến xe: {trip_info}
Số lượng ghế: {seat_count} ghế
Ghế đã đặt: {seats_display}
Tổng tiền: {total_price:,.0f} VNĐ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Vé điện tử của bạn đã được xác nhận. Vui lòng xuất trình mã đặt chỗ này khi lên xe.

Chúc bạn có chuyến đi an toàn và vui vẻ!

Trân trọng,
Đội ngũ Hỗ trợ Khách hàng
"""
    
    return send_email(receiver_email, subject, body)

def send_booking_cancellation_email(
    receiver_email: str,
    booking_code: str,
    customer_name: str,
    cancellation_reason: str = None
) -> bool:
    """Gửi email thông báo hủy vé"""
    subject = f"Thông báo hủy vé - Mã đặt chỗ: {booking_code}"
    
    reason_text = f"\nLý do: {cancellation_reason}" if cancellation_reason else ""
    
    body = f"""
Kính gửi {customer_name},

Vé xe khách của bạn đã được HỦY thành công.

THÔNG TIN HỦY VÉ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mã đặt chỗ: {booking_code}
Trạng thái: ĐÃ HỦY{reason_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Nếu bạn đã thanh toán, chúng tôi sẽ xử lý hoàn tiền theo chính sách hoàn vé.

Nếu có bất kỳ thắc mắc nào, vui lòng liên hệ bộ phận chăm sóc khách hàng.

Trân trọng,
Đội ngũ Hỗ trợ Khách hàng
"""
    
    return send_email(receiver_email, subject, body)

def send_booking_refund_email(
    receiver_email: str,
    booking_code: str,
    customer_name: str,
    refund_amount: float
) -> bool:
    """Gửi email thông báo hoàn tiền"""
    subject = f"Xác nhận hoàn tiền - Mã đặt chỗ: {booking_code}"
    
    body = f"""
Kính gửi {customer_name},

Chúng tôi xác nhận đã xử lý yêu cầu HOÀN TIỀN của bạn.

THÔNG TIN HOÀN TIỀN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mã đặt chỗ: {booking_code}
Số tiền hoàn: {refund_amount:,.0f} VNĐ
Trạng thái: ĐÃ HOÀN TIỀN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Số tiền sẽ được hoàn vào tài khoản của bạn trong vòng 3-5 ngày làm việc.

Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!

Trân trọng,
Đội ngũ Hỗ trợ Khách hàng
"""
    
    return send_email(receiver_email, subject, body)


def get_current_datetime() -> datetime:
    """Lấy thời gian hiện tại (UTC)"""
    return datetime.utcnow()

def format_datetime(dt: datetime, format_str: str = "%d/%m/%Y %H:%M:%S") -> str:
    """Format datetime thành string"""
    return dt.strftime(format_str)

def generate_otp_code(length: int = 6) -> str:
    """
    Tạo mã OTP ngẫu nhiên
    """
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(
    receiver_email: str,
    otp_code: str,
    otp_type: str,
    expiry_minutes: int = 5
) -> bool:
    type_display = {
        "booking": "XÁC THỰC ĐẶT VÉ",
        "refund": "XÁC THỰC HOÀN TIỀN",
        "update": "XÁC THỰC CẬP NHẬT THÔNG TIN"
    }.get(otp_type, "XÁC THỰC")
    
    subject = f"Mã OTP xác thực - {type_display}"
    
    body = f"""
Xin chào,

Mã OTP của bạn để {type_display}:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        MÃ OTP: {otp_code}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ Mã OTP này có hiệu lực trong {expiry_minutes} phút.

⚠️ LƯU Ý:
- KHÔNG chia sẻ mã OTP này với bất kỳ ai
- Nếu bạn không yêu cầu mã OTP này, vui lòng bỏ qua email

Trân trọng,
Đội ngũ Hỗ trợ Khách hàng
"""
    
    return send_email(receiver_email, subject, body)

def validate_otp_format(otp: str) -> tuple[bool, str]:
    """
    Kiểm tra format OTP
    """
    if not otp:
        return False, "Mã OTP không được để trống"
    
    if not otp.isdigit():
        return False, "Mã OTP chỉ được chứa số"
    
    if len(otp) < 6 or len(otp) > 8:
        return False, "Mã OTP phải có độ dài 6-8 ký tự"
    
    return True, ""
