from fastapi import Request, Response, HTTPException
import httpx
from .setting import settings

async def _find_upstream(path: str) -> tuple[str, str]:
    # match prefix dài nhất: /auth hoặc /tuition
    matches = [(p, b) for p, b in settings.ROUTES.items() if path.startswith(p)]
    if not matches:
        raise HTTPException(404, "Không tìm thấy đường dẫn")
    prefix, base = max(matches, key=lambda x: len(x[0]))
    suffix = path[len(prefix):] or "/"
    return base, suffix

async def proxy_request(request: Request) -> Response:
    upstream, suffix = await _find_upstream(request.url.path)
    target = f"{upstream}{suffix}"
    if request.url.query:
        target += f"?{request.url.query}"

    headers = dict(request.headers)
    headers.pop("host", None)
    # forward IP/proto
    if request.client:
        headers["x-forwarded-for"] = request.client.host
    headers["x-forwarded-proto"] = request.url.scheme

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.request(
            request.method,
            target,
            headers=headers,
            content=await request.body(),
        )
        excluded = {"connection", "keep-alive", "transfer-encoding", "content-encoding"}
        out_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=out_headers,
            media_type=resp.headers.get("content-type"),
        )
