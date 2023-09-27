from typing import Any
from dto.objects import DataResponse
from dto.responses import LoginResponseDto
from fastapi import status
from fastapi.requests import Request
from stores import user_store


def exclude(iterable, exclude: list) -> list:
    return list(map(lambda item: item.model_dump(exclude=exclude), iterable))


def create_200_response(message: str | None = None, data: Any = None):
    return DataResponse(status=status.HTTP_200_OK, message=message, data=data)


def create_201_response(message: str | None = None, data: Any = None):
    return DataResponse(status=status.HTTP_201_CREATED, message=message, data=data)


def create_login_response(login_response: LoginResponseDto):
    return create_200_response(message="Login successfully", data=login_response)

def is_email_unique(email: str):
    for user in user_store:
        if user.email == email:
            return False
    return True
