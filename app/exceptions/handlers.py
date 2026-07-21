from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import traceback
from app.core.logging_config import logger

async def http_exception_handler(request:Request, exc:HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "path": request.url.path,
            "method": request.method,
            "data": None
        }
    )

async def global_exception_handler(request:Request, exc:Exception):
    logger.exception(exc) 

    return JSONResponse(
        status_code=500,
        content={
            "success":False,
            "message": "Internal Server Error",
            "path": request.url.path,
            "method": request.method,
            "data": None
        }
    )



# logger.exception()? This is a special logging method.It automatically logs exception message and complete traceback
# For example:

# try:
#     1/0
# except Exception as e:
#     logger.exception(e)

# Log becomes
# ERROR division by zero

# Traceback...

# ...