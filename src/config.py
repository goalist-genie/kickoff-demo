import secrets
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPEN_API_KEY: str = "<edit me>"
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str = "this_is_my_super_secret_key"
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    # required
    SERVER_NAME: str = "LangChain"
    SERVER_HOST: str = "http://localhost:8000"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, tuple)):
            return v
        raise ValueError(v)

    DEBUG: bool = True

    PUBLIC_URLS: list[str] = [
        "/docs",
        "/openapi.json",
        API_V1_STR + "/login",
        API_V1_STR + "/register",
        # API_V1_STR + "/projects",
    ]


settings = Settings()
