from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import NotFoundException
from dto.objects import DataResponse

def handle_not_found(request: Request, exc: NotFoundException):
    response = DataResponse(status=exc.status_code, message=exc.detail)
    delattr(response, "data")
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())