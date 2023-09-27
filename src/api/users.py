from fastapi import APIRouter
from config import settings
from dto.objects import User, DataResponse
from dto.requests import CreateUserDto, LoginDto
from dto.responses import LoginResponseDto
from auth import create_access_token
from utils import create_201_response, create_200_response, create_login_response
from exceptions import BadRequestException
from stores import user_store
import logging

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix=settings.API_V1_STR)


def _authenticate_user(email: str, password: str) -> User:
    for user in user_store:
        if user.email == email and user.password == password:
            return user
    raise BadRequestException("Wrong email or password")


@user_router.post("/register", response_model=DataResponse)
async def register_user(dto: CreateUserDto):
    user = User(**dto.model_dump())
    user_store.append(user)
    return create_201_response(message="User created successfully")


@user_router.post("/login", response_model=DataResponse)
async def login(login_dto: LoginDto):
    user: User = _authenticate_user(login_dto.email, login_dto.password)
    logger.info("user: %s", user)
    jwt_token = create_access_token(user)
    login_response = LoginResponseDto(
        access_token=jwt_token,
        email=user.email,
        full_name=user.full_name,
        user_id=user.id,
    )
    return create_login_response(login_response)
