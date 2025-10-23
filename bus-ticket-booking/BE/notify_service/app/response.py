from fastapi.responses import JSONResponse

def successResponse(status_code=200, headers={"Content-type": "application/json"}, msg="Thành công", data=None ):
    return JSONResponse( 
                    status_code=status_code, 
                    headers=headers,
                    content={
                                "status": "ok", 
                                "message": msg, 
                                "data": data
                            }
                    )

def errorResponse(status_code=401, headers={"Content-type": "application/json"}, msg="Thất bại"):
    return JSONResponse( 
                    status_code=status_code, 
                    headers=headers,
                    content={
                                "status": "failed", 
                                "message": msg, 
                                "data": None
                            }
                    )