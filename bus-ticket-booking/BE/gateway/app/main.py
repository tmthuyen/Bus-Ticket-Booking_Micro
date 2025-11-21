from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .setting import settings
from .security import needs_auth, verify_jwt
from .proxy import proxy_request


app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health(): return {"status": "ok"}

# wildcard: mọi request đi qua đây
@app.api_route("/{full_path:path}", methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD"])
async def gateway(full_path: str, request: Request):
    path = "/" + full_path
    # Tat authentication
    # if needs_auth(path):
    #     verify_jwt(request)
    return await proxy_request(request)
