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


class QAObject(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    question: str = None
    answer: str = None
    created_by: str = "System"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": uuid4().hex,
                    "question": "What is this project about?",
                    "answer": "This project is about ...",
                    "created_by": "System",
                }
            ]
        },
        "arbitrary_types_allowed": True,
    }


class Project(BaseModel):
    id: int = None
    project_name: str
    project_overview: str
    created_by: str = "System"
    documents: list[Document] = []
    qas: list[QAObject] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "project_name": "Project 1",
                    "project_overview": "This is project 1 overview",
                    "created_by": "System",
                }
            ]
        },
        "arbitrary_types_allowed": True,
    }
