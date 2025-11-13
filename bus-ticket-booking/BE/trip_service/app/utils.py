import datetime as dt
from datetime import datetime, timedelta, timezone 
from .config import settings
import re, unicodedata
from zoneinfo import ZoneInfo

_slug_re = re.compile(r"[^a-z0-9]+")  # chỉ giữ a-z0-9, cái khác -> '-'
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
 
def create_slug(s: str) -> str:
    """Tạo slug từ chuỗi đầu vào."""
    if not s:
        return ""
    # bỏ dấu
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower()
    s = _slug_re.sub("-", s)          # thay cụm ký tự lạ/space bằng '-'
    s = s.strip("-")
    s = re.sub(r"-{2,}", "-", s)      # gộp '---' -> '-'
    return s


def local_date_to_utc_range(date_str: str, tz: ZoneInfo = VN_TZ) -> tuple[dt.datetime, dt.datetime]:
    """
    Nhận 'YYYY-MM-DD' hoặc ISO datetime (có/không offset).
    Trả về (start_utc_naive, end_utc_naive) để query MySQL DATETIME (UTC-naive).
    """
    s = date_str.strip()
    # Trường hợp chỉ có ngày
    if len(s) == 10 and s[4] == "-" and s[7] == "-":
        d = datetime.fromisoformat(s)
        start_local = datetime.combine(d, datetime.min.time(), tzinfo=tz)
        end_local   = start_local + timedelta(days=1)
    else:
        # Có thời gian: cố gắng parse ISO
        # Nếu không có offset, mặc định là local VN
        v = datetime.fromisoformat(s)
        if v.tzinfo is None:
            v = v.replace(tzinfo=tz)
        # Lấy ngày local từ thời điểm v
        d = v.astimezone(tz).date()
        start_local = datetime.combine(d, datetime.min.time(), tzinfo=tz)
        end_local   = start_local + timedelta(days=1)

    start_utc = start_local.astimezone(timezone.utc)
    end_utc   = end_local.astimezone(timezone.utc)
    # MySQL DATETIME đang lưu UTC-naive → strip tzinfo
    return (start_utc.replace(tzinfo=None), end_utc.replace(tzinfo=None))