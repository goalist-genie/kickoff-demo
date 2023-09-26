from typing import Any
from dto.objects import DataResponse
from fastapi import status


def exclude(iterable, exclude: list) -> list:
    return list(map(lambda item: item.model_dump(exclude=exclude), iterable))

def create_200_response(message: str | None = None, data: Any = None):
    return DataResponse(status=status.HTTP_200_OK, message=message, data=data)


def create_201_response(message: str | None = None, data: Any = None):
    return DataResponse(status=status.HTTP_201_CREATED, message=message, data=data)
