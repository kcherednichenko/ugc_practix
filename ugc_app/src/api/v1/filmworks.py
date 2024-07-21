from typing import Annotated
from uuid import UUID
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response, HTTPException
from pydantic import BaseModel

from models.users import User
from api.v1.dependencies import get_authenticated_user
from services.filmworks import get_filmwork_service, FilmworkService


router = APIRouter()


class ScoreRequestBody(BaseModel):
    score: int


class ScoreResponseBody(BaseModel):
    score: int
    filmwork_id: UUID


class AvgScoreResponseBody(BaseModel):
    avg_score: float


@router.get("/{filmwork_id}/average-score")
async def get_filmwork_average_score(
    filmwork_id: UUID,
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
) -> AvgScoreResponseBody:
    avg_score = await filmwork_service.get_average_score(filmwork_id)
    if not avg_score:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="filmwork not found or has no scores")
    return AvgScoreResponseBody(avg_score=avg_score)


@router.post("/{filmwork_id}/score")
async def add_score(
    filmwork_id: UUID,
    score_request: ScoreRequestBody,
    user: Annotated[User, Depends(get_authenticated_user)],
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
) -> ScoreResponseBody:
    await filmwork_service.upsert_user_score(filmwork_id, user.id, score_request.score)
    return ScoreResponseBody(score=score_request.score, filmwork_id=filmwork_id)


@router.delete("/{filmwork_id}/score")
async def delete_score(
    filmwork_id: UUID,
    user: Annotated[User, Depends(get_authenticated_user)],
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
) -> Response:
    await filmwork_service.delete_user_score(filmwork_id, user.id)
    return Response(status_code=HTTPStatus.NO_CONTENT)
