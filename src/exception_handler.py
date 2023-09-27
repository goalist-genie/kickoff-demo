from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import NotFoundException, UnauthorizedException, BadRequestException
from dto.objects import DataResponse


def handle_not_found(request: Request, exc: NotFoundException):
    response = DataResponse(status=exc.status_code, message=exc.detail)
    delattr(response, "data")
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())


def handle_401(request: Request, exc: UnauthorizedException):
    response = DataResponse(status=exc.status_code, message=exc.detail)
    delattr(response, "data")
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())


def handle_400(request: Request, exc: BadRequestException):
    response = DataResponse(status=exc.status_code, message=exc.detail)
    delattr(response, "data")
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())
