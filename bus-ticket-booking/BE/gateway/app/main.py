from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter
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
app.add_exception_handler(RateLimitExceeded, limiter._rate_limit_exceeded_handler)
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
    return {"status": "ok"}

# Wildcard: mọi request đi qua đây
# Ví dụ giới hạn: 100 request / phút / IP
@app.api_route("/{full_path:path}", methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD"])
@limiter.limit("50/minute")
async def gateway(full_path: str, request: Request):
    path = "/" + full_path

    # Kiểm tra JWT cho các path không nằm trong ALLOWLIST
    if needs_auth(path):
        verify_jwt(request)

    # Proxy request sang backend tương ứng
    return await proxy_request(request)
