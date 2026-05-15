# RESPONSE HELPER - CÁC HÀM HỖ TRỢ TRẢ VỀ RESPONSE

from fastapi.responses import JSONResponse
from typing import Any, Optional, Dict

def successResponse(
    status_code: int = 200, 
    headers: Dict[str, str] = {"Content-type": "application/json"}, 
    msg: str = "Thành công", 
    data: Optional[Any] = None
) -> JSONResponse:
    """Trả về response thành công với format chuẩn
    
    Args:
        status_code: HTTP status code (mặc định 200)
        headers: HTTP headers
        msg: Thông báo thành công
        data: Dữ liệu trả về
        
    Returns:
        JSONResponse: Response với format chuẩn
    """
    return JSONResponse( 
        status_code=status_code, 
        headers=headers,
        content={
            "success": True, 
            "message": msg, 
            "data": data
        }
    )

def errorResponse(
    status_code: int = 400, 
    headers: Dict[str, str] = {"Content-type": "application/json"}, 
    msg: str = "Thất bại",
    data: Optional[Any] = None
) -> JSONResponse:
    """Trả về response lỗi với format chuẩn
    
    Args:
        status_code: HTTP status code (mặc định 400)
        headers: HTTP headers  
        msg: Thông báo lỗi
        
    Returns:
        JSONResponse: Response với format chuẩn
    """
    return JSONResponse( 
        status_code=status_code, 
        headers=headers,
        content={
            "success": False, 
            "message": msg, 
            "data": data
        }
    )