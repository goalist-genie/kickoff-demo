# OPEN_API_KEY = "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"

# from langchain.llms import OpenAI

# llm = OpenAI(openai_api_key="org-9U0wmS9Sq2KobC5zIOvu3HuL")

# result = llm.predict(input("Please enter a sentence:"))

# print("Result:", result)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from api import projects
import exceptions as custom_exceptions
import exception_handler as handlers


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle exception
app.add_exception_handler(custom_exceptions.NotFoundException, handlers.handle_not_found)


@app.get("/")
def read_root():
    logger.info("Hello World")
    return {"Hello": "World"}


app.include_router(projects.project_router, tags=["projects"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", reload=settings.DEBUG, log_config="./log-config.yaml")
