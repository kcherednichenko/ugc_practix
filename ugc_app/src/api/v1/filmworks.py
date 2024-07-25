from datetime import datetime
from http import HTTPStatus
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict

from models.users import AuthenticatedUser
from api.v1.dependencies import get_authenticated_user
from services.filmworks import FilmworkService, get_filmwork_service
from services.users import get_user_service, UserService

router = APIRouter()


class ScoreRequestBody(BaseModel):
    score: int


class ScoreResponseBody(BaseModel):
    score: int
    filmwork_id: UUID


class AvgScoreResponseBody(BaseModel):
    avg_score: float


class ReviewRequestBody(BaseModel):
    title: str
    text: str


class ReviewResponseBody(BaseModel):
    title: str
    filmwork_id: UUID

    model_config = ConfigDict(from_attributes=True)


class FullReviewResponseBody(BaseModel):
    id: UUID
    filmwork_id: UUID
    title: str
    text: str
    created_at: datetime
    likes: List


@router.get("/{filmwork_id}/average-score")
async def get_filmwork_average_score(
    filmwork_id: UUID,
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
) -> AvgScoreResponseBody:
    avg_score = await filmwork_service.get_average_score(filmwork_id)
    if not avg_score:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="filmwork not found or has no scores",
        )
    return AvgScoreResponseBody(avg_score=avg_score)


@router.post("/{filmwork_id}/score")
async def add_score(
    filmwork_id: UUID,
    score_request: ScoreRequestBody,
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
) -> ScoreResponseBody:
    await filmwork_service.upsert_user_score(filmwork_id, user.id, score_request.score)
    return ScoreResponseBody(score=score_request.score, filmwork_id=filmwork_id)


@router.delete("/{filmwork_id}/score")
async def delete_score(
    filmwork_id: UUID,
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
) -> Response:
    await filmwork_service.delete_user_score(filmwork_id, user.id)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.get("/{filmwork_id}/reviews")
async def get_reviews(
    filmwork_id: UUID,
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
    order: str | None = None,
) -> List[FullReviewResponseBody]:
    reviews = await filmwork_service.get_reviews(filmwork_id, order)
    full_reviews = []
    for review in reviews:
        full_reviews.append(FullReviewResponseBody(filmwork_id=filmwork_id, **review.__dict__))
    return full_reviews


@router.post("/{filmwork_id}/reviews")
async def add_review(
    filmwork_id: UUID,
    review_request: ReviewRequestBody,
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> ReviewResponseBody:
    await filmwork_service.upsert_review(filmwork_id, user.id, review_request.title, review_request.text)
    await user_service.upsert_review(filmwork_id, user.id, review_request.title, review_request.text)
    return ReviewResponseBody(title=review_request.title, filmwork_id=filmwork_id)


@router.delete("/{filmwork_id}/reviews")
async def delete_review(
    filmwork_id: UUID,
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> Response:
    await filmwork_service.delete_review(filmwork_id, user.id)
    await user_service.delete_review(filmwork_id, user.id)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.post("/{filmwork_id}/reviews/{user_id}/likes")
async def like_review(
    filmwork_id: UUID,
    user_id: UUID,
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> Response:
    await filmwork_service.like_review(filmwork_id, user_id, user.id)
    await user_service.like_review(filmwork_id, user_id, user.id)
    return Response(status_code=HTTPStatus.CREATED)


@router.delete("/{filmwork_id}/reviews/{user_id}/likes")
async def delete_review_like(
    filmwork_id: UUID,
    user_id: UUID,
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    filmwork_service: Annotated[FilmworkService, Depends(get_filmwork_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> Response:
    await filmwork_service.delete_review_like(filmwork_id, user_id, user.id)
    await user_service.delete_review_like(filmwork_id, user_id, user.id)
    return Response(status_code=HTTPStatus.NO_CONTENT)
