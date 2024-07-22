from contextlib import asynccontextmanager

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from models.filmworks import Filmwork, FilmworkScore
from settings import settings
from api.v1 import filmworks


@asynccontextmanager
async def lifespan(_: FastAPI):
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        settings.mongo_host, settings.mongo_port
    )
    await init_beanie(
        database=client[settings.mongo_db], document_models=[Filmwork, FilmworkScore]
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
