from fastapi import APIRouter, status, UploadFile
from config import settings
from dto.objects import Project, Document
from utils import create_200_response, exclude
from dto.objects import DataResponse
from exceptions import NotFoundException
import logging

logger = logging.getLogger(__name__)

project_router = APIRouter(prefix=settings.API_V1_STR)

global projects_store
projects_store: list[Project] = [
    Project(id=1, project_name="Project A"),
    Project(id=2, project_name="Project B"),
    Project(id=3, project_name="Project C"),
]


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
    "/projects", response_model=DataResponse, response_model_exclude_none=True
)
async def create_project(dto: Project) -> DataResponse:
    id = generate_id()
    new_project = Project(
        id=id, project_name=dto.project_name, created_by=dto.created_by
    )
    projects_store.append(new_project)
    return DataResponse(status=status.HTTP_200_OK, message="create successfully")


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
