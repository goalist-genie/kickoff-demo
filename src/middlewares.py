from fastapi import Request
from fastapi.responses import JSONResponse
from auth import verify_token
from exceptions import UnauthorizedException
from dto.objects import DataResponse
from config import settings

import logging
logger = logging.getLogger(__name__)

async def authenticate_middleware(request: Request, call_next):
    logger.info("Performing authentication")
    authentication = request.headers.get("Authorization")
    path = request.scope["path"]
    logger.info("path: %s", path)
    if path in settings.PUBLIC_URLS:
        return await call_next(request)
    
    
    try:
        if not authentication:
            raise UnauthorizedException()
    
        authentication = authentication.split(" ")
        if len(authentication) != 2 or authentication[0] != "Bearer":
            raise Exception("Invalid token")
    except:
        content = DataResponse(status=401, message="Unauthorized").model_dump(exclude=["data"])
        return JSONResponse(status_code=401, content=content)
    
    token = authentication[1]
    current_user = verify_token(token)
    request.state.user = current_user
    return await call_next(request)