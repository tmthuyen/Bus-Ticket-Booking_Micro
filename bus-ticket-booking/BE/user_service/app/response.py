from fastapi.responses import JSONResponse, Response
from typing import Any, Optional

def response_authentication(
    response: Response,
    *,
    msg: str = "Thành công",
    data: Optional[Any] = None,
    status_code: int = 200,
    headers: Optional[dict[str, str]] = None,
):
    # set status + headers vào response HIỆN TẠI (đã có cookie)
    response.status_code = status_code
    if headers:
        for k, v in headers.items():
            response.headers[k] = v
    # trả dict -> FastAPI dùng chính response này để gửi
    return {
        "success": True,
        "message": msg,
        "data": data,
    }

def successResponse(status_code=200, headers={"Content-type": "application/json"}, msg="Thành công", data=None, response=Response ):
    return JSONResponse( 
                    status_code=status_code, 
                    headers=headers,
                    content={
                                "success": True, 
                                "message": msg, 
                                "data": data
                            }
                    )

def errorResponse(status_code=400, headers={"Content-type": "application/json"}, msg="Thất bại", errors=None):
    return JSONResponse( 
                    status_code=status_code, 
                    headers=headers,
                    content={
                                "success": False, 
                                "message": msg, 
                                "data": None,
                                "errors": errors
                            }
                    ) 