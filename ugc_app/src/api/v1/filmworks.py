from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models.users import User
from models.filmworks import Filmwork, FilmworkScore
from api.v1.dependencies import get_authenticated_user


router = APIRouter()


class ScoreRequest(BaseModel):
    score: int


class ScoreResponse(BaseModel):
    score: int
    filmwork_id: UUID


@router.post("/{filmwork_id}/score")
async def add_score(
    filmwork_id: UUID,
    score_request: ScoreRequest,
    user: Annotated[User, Depends(get_authenticated_user)],
) -> ScoreResponse:
    await Filmwork(id=filmwork_id, scores=[FilmworkScore(id=user.id, score=score_request.score)]).save()
    return ScoreResponse(score=score_request.score, filmwork_id=filmwork_id)
