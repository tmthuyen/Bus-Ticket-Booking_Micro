from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .setting import settings
from .security import needs_auth, verify_jwt
from .proxy import proxy_request

# Limiter: key theo IP client
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title=settings.APP_NAME)

# Gắn limiter vào app state + middleware + handler 429
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check: ví dụ cho phép tối đa 10 request/phút/IP
@app.get("/healthz")
@limiter.limit("10/minute")
def health(request: Request): 
    """Kiểm tra gateway dịch vụ"""
    return {"status": "ok"}


@app.post("/momo-callback")
def test_payment_callback(request: Request):
    """ Xử lý callback từ MoMo (chỉ ví dụ) """
    print("Received MoMo payment callback")
    print("Headers:", request.headers)
    print("Body:", request.body())
    return {"message": "MoMo callback received"}

# Wildcard: mọi request đi qua đây
# Ví dụ giới hạn: 100 request / phút / IP
@app.api_route("/{full_path:path}", methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD"])
@limiter.limit("50/minute")
async def gateway(full_path: str, request: Request):
    """Xử lý proxy tất cả các request còn lại"""
    path = "/" + full_path

    # Kiểm tra JWT cho các path không nằm trong ALLOWLIST
    if needs_auth(path):
        verify_jwt(request)

    # Proxy request sang backend tương ứng
    return await proxy_request(request)
