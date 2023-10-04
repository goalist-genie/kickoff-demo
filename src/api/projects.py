from fastapi import APIRouter, status, UploadFile, Form, File
from fastapi.requests import Request
from config import settings
from dto.objects import Project, Document, User
from dto.requests import ProjectUpsertDto
from utils import create_200_response, exclude
from dto.objects import DataResponse
from exceptions import NotFoundException
from stores import projects_store
import logging


logger = logging.getLogger(__name__)

project_router = APIRouter(prefix=settings.API_V1_STR)


def _get_project_by_id(project_id: int) -> Project:
    for project in projects_store:
        if project.id == project_id:
            return project

    raise NotFoundException()


def generate_id() -> int:
    return len(projects_store) + 1


def filter_projects(search: str) -> list[Project]:
    if search:
        result_set = filter(
            lambda project: search.lower() in project.project_name.lower(),
            projects_store,
        )
        return exclude(result_set, exclude=["documents"])
    return exclude(projects_store, exclude=["documents"])


@project_router.get(
    "/projects", response_model=DataResponse, response_model_exclude_none=True
)
async def get_projects(search: str = None) -> DataResponse:
    logger.info("search: %s", search)
    data = filter_projects(search)
    return create_200_response(message="get successfully", data=data)


@project_router.post(
    "/projects",
    response_model=DataResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    request: Request,
    project_name: str = Form(),
    project_overview: str = Form(),
    files: list[UploadFile] = File(),
) -> DataResponse:
    id = generate_id()
    current_user: User = request.state.user
    new_project = Project(
        id=id,
        project_name=project_name,
        project_overview=project_overview,
        created_by=current_user.full_name,
    )

    if files:
        for file in files:
            document = Document(
                document_name=file.filename,
                created_by=current_user.full_name,
                file=file,
            )
            new_project.documents.append(document)

    projects_store.append(new_project)
    return DataResponse(status=status.HTTP_201_CREATED, message="create successfully")


@project_router.get(
    "/projects/{project_id}",
    response_model=DataResponse,
    response_model_exclude_none=True,
)
async def get_project_by_id(project_id: int) -> DataResponse:
    project = _get_project_by_id(project_id)
    if not project:
        raise NotFoundException()
    return DataResponse(
        status=status.HTTP_200_OK, message="get successfully", data=project
    )


@project_router.put(
    "/projects/{project_id}",
    response_model=DataResponse,
    response_model_exclude_none=True,
)
async def add_documents_to_project(
    project_id: int, files: list[UploadFile]
) -> DataResponse:
    project = _get_project_by_id(project_id)
    for file in files:
        document = Document(document_name=file.filename, created_by="System", file=file)
        project.documents.append(document)
    return DataResponse(status=status.HTTP_200_OK, message="Update successfully")


@project_router.delete(
    "/projects/{project_id}",
    response_model=DataResponse,
)
async def delete_project_by_id(project_id: int):
    found = _get_project_by_id(project_id)
    projects_store.remove(found)
    return create_200_response(message="delete successfully")
