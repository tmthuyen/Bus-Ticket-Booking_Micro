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
    # 1. Tìm upstream
    try:
        upstream, suffix = await _find_upstream(request.url.path)
    except HTTPException:
        # giữ nguyên 404 từ _find_upstream
        raise
    except Exception as e:
        # lỗi bất ngờ khi route → 500
        raise HTTPException(500, f"Lỗi định tuyến gateway: {e}") from e

    # 2. Build URL đích
    target = f"{upstream}{suffix}"
    if request.url.query:
        target += f"?{request.url.query}"

    # 3. Forward header
    headers = dict(request.headers)
    headers.pop("host", None)
    if request.client:
        headers["x-forwarded-for"] = request.client.host
    headers["x-forwarded-proto"] = request.url.scheme

    # 4. Gọi service con với httpx, có try/catch rõ ràng
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.request(
                request.method,
                target,
                headers=headers,
                content=await request.body(),
            )
    except httpx.ReadTimeout:
        # service con không trả lời kịp → 504
        raise HTTPException(
            status_code=504,
            detail=f"Upstream timeout khi gọi {target}"
        )
    except httpx.ConnectError:
        # không kết nối được (service down / DNS lỗi) → 502
        raise HTTPException(
            status_code=502,
            detail=f"Không kết nối được upstream {target}"
        )
    except httpx.RequestError as exc:
        # lỗi HTTP chung → 502
        raise HTTPException(
            status_code=502,
            detail=f"Lỗi khi gọi upstream {target}: {exc}"
        )

    # 5. Trả response xuống client
    excluded = {"connection", "keep-alive", "transfer-encoding", "content-encoding"}
    out_headers = {
        k: v for k, v in resp.headers.items() if k.lower() not in excluded
    }

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=out_headers,
        media_type=resp.headers.get("content-type"),
    )
