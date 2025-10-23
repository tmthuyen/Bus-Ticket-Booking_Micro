from email.mime.multipart import MIMEMultipart
# import random
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo 
import smtplib, ssl
from email.mime.text import MIMEText 
import secrets 
from . import schemas 

DIGITS = "0123456789"

VN = ZoneInfo("Asia/Ho_Chi_Minh")
VIETNAM_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

def now_utc() -> datetime:
    return datetime.now(timezone.utc)          # aware UTC

def now_vn() -> datetime:
    return now_utc().astimezone(VN)

def to_vn(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(VIETNAM_TZ)

# expiry time
def get_expiry(cur_dt: datetime, minutes=5) -> datetime:
    return cur_dt + timedelta(minutes=minutes)

# current time 
def get_current_time():
    return datetime.now()

def generate_otp(length: int = 6) -> str:
    return "".join(secrets.choice(DIGITS) for _ in range(length))
# def generate_otp(length=6):
#     return f"{random.randint(0, 10**length - 1):0{length}d}"

def send_email(receiver_email: str, subject: str, body: str):
    sender_email = "minhtuank27tdtu@gmail.com"
    password = "scxwnfestbszztcf"
    port = 465  # For SSL
 
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl.create_default_context()) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())



def send_otp_email(receiver_email: str, otp_code: str):
    sender_email = "minhtuank27tdtu@gmail.com"
    password = "scxwnfestbszztcf"
    port = 465  # For SSL

    subject = "Mã OTP của bạn để xác thực giao dịch"
    body = f"Mã OTP của bạn là: {otp_code}. Mã sẽ hết hạn trong 5 phút."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl.create_default_context()) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully")

def send_success_email(receiver_email: str):
    sender_email = "minhtuank27tdtu@gmail.com"
    password = "scxwnfestbszztcf"
    port = 465  # For SSL

    subject = "Payment Successful"
    body = "Your payment has been processed successfully."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl.create_default_context()) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Success email sent successfully")
    
     
def fmt_currency_vnd(amount) -> str:
    try:
        # amount có thể là str/Decimal/float
        amount = float(amount)
    except Exception:
        return str(amount)
    return f"{amount:,.0f} VND".replace(",", ".")

def build_email_html_text(body_obj: schemas.PaymentNotification) -> tuple[str, str]:
    payer_name = body_obj.payer_name or body_obj.student_id
    created_vn = body_obj.created_at  # đổi sang giờ VN
    amount_vnd = fmt_currency_vnd(body_obj.amount)

    # --- Plain text (fallback) ---
    text = f"""Kính gửi {payer_name},

Giao dịch thanh toán học phí cho kỳ {body_obj.term} đã được thực hiện thành công.

Chi tiết:
- Mã thanh toán: {body_obj.payment_id}
- Mã người thanh toán: {body_obj.payer_id}
- Người thanh toán: {body_obj.payer_name or '-'}
- Mã sinh viên: {body_obj.student_id}
- Họ và tên: {body_obj.full_name}
- Kỳ học: {body_obj.term}
- Số tiền: {amount_vnd}
- Ngày thực hiện: {created_vn}
- Trạng thái: {body_obj.payment_status}

Nếu bạn có bất kỳ câu hỏi nào, xin vui lòng liên hệ với chúng tôi.

Trân trọng,
TDTU Tuition Payment Team
"""

    # --- HTML ---
    html = f"""\
<!doctype html>
<html lang="vi">
  <head>
    <meta charset="utf-8" />
    <meta name="x-apple-disable-message-reformatting">
    <meta name="format-detection" content="telephone=no,date=no,address=no,email=no,url=no">
    <title>{body_obj.subject}</title>
    <style>
      body {{ margin:0; padding:24px; background:#f6f7f9; font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; }}
      .card {{
        max-width:620px; margin:0 auto; background:#fff; border-radius:16px;
        box-shadow:0 4px 20px rgba(0,0,0,.06); overflow:hidden; border:1px solid #eef0f3;
      }}
      .header {{ padding:20px 24px; background:#0a66c2; color:#fff; }}
      .header h1 {{ margin:0; font-size:18px; font-weight:700; }}
      .content {{ padding:24px; color:#1f2328; }}
      .content p {{ margin:0 0 12px; line-height:1.6; }}
      .table {{ width:100%; border-collapse:collapse; margin-top:12px; }}
      .table th, .table td {{ text-align:left; padding:10px 12px; border-bottom:1px solid #eef0f3; vertical-align:top; }}
      .label {{ color:#6b7280; width:38%; white-space:nowrap; }}
      .value {{ color:#111827; font-weight:600; }}
      .footer {{ padding:16px 24px; color:#6b7280; font-size:12px; background:#fafbfc; }}
      .pill {{ display:inline-block; padding:2px 10px; border-radius:999px; font-weight:600; font-size:12px; }}
      .pill-success {{ background:#ecfdf5; color:#047857; }}
      .pill-failed {{ background:#fef2f2; color:#b91c1c; }}
      .pill-processing {{ background:#eff6ff; color:#1d4ed8; }}
    </style>
  </head>
  <body>
    <div class="card">
      <div class="header">
        <h1>Thanh toán học phí TDTU</h1>
      </div>
      <div class="content">
        <p>Kính gửi <strong>{payer_name}</strong>,</p>
        <p>Giao dịch thanh toán học phí cho kỳ <strong>{body_obj.term}</strong> đã được thực hiện.</p>

        <table class="table" role="presentation">
          <tr>
            <td class="label">Mã thanh toán</td>
            <td class="value">{body_obj.payment_id}</td>
          </tr>
          <tr>
            <td class="label">Người thanh toán</td>
            <td class="value">{body_obj.payer_name or '-' } ({body_obj.payer_id})</td>
          </tr>
          <tr>
            <td class="label">Mã sinh viên</td>
            <td class="value">{body_obj.student_id}</td>
          </tr>
          <tr>
            <td class="label">Họ và tên</td>
            <td class="value">{body_obj.full_name}</td>
          </tr>
          <tr>
            <td class="label">Kỳ học</td>
            <td class="value">{body_obj.term}</td>
          </tr>
          <tr>
            <td class="label">Số tiền</td>
            <td class="value">{amount_vnd}</td>
          </tr>
          <tr>
            <td class="label">Ngày thực hiện</td>
            <td class="value">{created_vn}</td>
          </tr>
          <tr>
            <td class="label">Trạng thái</td>
            <td class="value">
              <span class="pill {('pill-success' if body_obj.payment_status=='SUCCESS' else ('pill-processing' if body_obj.payment_status=='PROCESSING' else 'pill-failed'))}">
                {body_obj.payment_status}
              </span>
            </td>
          </tr>
        </table>

        <p style="margin-top:16px;">Nếu bạn có bất kỳ câu hỏi nào, xin vui lòng liên hệ với chúng tôi.</p>
        <p>Trân trọng,<br/>TDTU Tuition Payment Team</p>
      </div>
      <div class="footer">
        Email này được gửi tự động, vui lòng không trả lời trực tiếp.
      </div>
    </div>
  </body>
</html>
"""
    return html, text

def send_email_plus(receiver_email: str, subject: str, html_body: str, text_body: str):
    # sender_email = os.getenv("SMTP_USER", "no-reply@example.com")  # ✔ lấy từ env
    # password = os.getenv("SMTP_PASS")  # ✔ app password (Gmail) trong env
    # port = int(os.getenv("SMTP_SSL_PORT", "465"))
    # smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    sender_email = "minhtuank27tdtu@gmail.com"
    password = "scxwnfestbszztcf"
    port = 465  # For SSL
    smtp_host = "smtp.gmail.com"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Reply-To"] = sender_email

    # phần text trước, html sau
    part_text = MIMEText(text_body, "plain", _charset="utf-8")
    part_html = MIMEText(html_body, "html", _charset="utf-8")
    msg.attach(part_text)
    msg.attach(part_html)

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, port, context=ctx) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())

def send_email_payment(body_obj):
    subject = getattr(body_obj, "subject", "Thanh toán học phí TDTU")
    html_body, text_body = build_email_html_text(body_obj)
    send_email_plus(body_obj.email, subject, html_body, text_body)
    return {"subject": subject, "receiver_email": body_obj.email, "html_body": html_body, "text_body": text_body}