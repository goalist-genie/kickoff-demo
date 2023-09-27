from pydantic import BaseModel, Field, EmailStr
from fastapi import UploadFile
from typing import Any
from uuid import uuid4


class DataResponse(BaseModel):
    status: int = 200
    message: str = None
    data: object = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": 200, "message": "MESSAGE", "data": {"key": "value"}}
            ]
        },
        "arbitrary_types_allowed": True,
    }


class User(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    full_name: str
    email: EmailStr
    password: str


class Document(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    document_name: str
    created_by: str
    file: UploadFile = Field(exclude=True)


class Project(BaseModel):
    id: int = None
    project_name: str
    created_by: str = "System"
    documents: list[Document] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "project_name": "Project 1",
                    "created_by": "user1",
                }
            ]
        },
        "arbitrary_types_allowed": True,
    }
