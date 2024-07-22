from contextlib import asynccontextmanager
from http import HTTPStatus
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
import sentry_sdk

from models.filmworks import Filmwork, FilmworkScore
from models.users import User
from settings import settings
from loggers import setup_logging
from api.v1 import filmworks, users

setup_logging()
logger = logging.getLogger(__name__)


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        settings.mongo_host, settings.mongo_port
    )
    await init_beanie(
        database=client[settings.mongo_db],
        document_models=[Filmwork, FilmworkScore, User],
    )
    yield
    client.close()


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
app.include_router(filmworks.router, prefix="/api/v1/filmworks", tags=["filmworks"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.middleware("http")
async def before_request(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        return ORJSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"detail": "X-Request-Id is required"},
        )
    return await call_next(request)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    logger.error(
        "Exception has occurred when handled request to %s: %s", request.url, exc
    )
    return ORJSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"detail": "internal server error"},
    )
