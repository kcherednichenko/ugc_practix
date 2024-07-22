from typing import Annotated, List
from uuid import UUID
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from models.users import AuthenticatedUser
from api.v1.dependencies import get_authenticated_user
from services.users import get_user_service, UserService

router = APIRouter()


class UserBookmarkRequestBody(BaseModel):
    filmwork_id: UUID


class UserBookmarksResponseBody(BaseModel):
    filmworks: List[UUID]


@router.get("/bookmarks")
async def get_bookmarks(
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserBookmarksResponseBody:
    bookmarks = await user_service.get_bookmarks(user.id)
    return UserBookmarksResponseBody(filmworks=bookmarks)


@router.post("/bookmarks")
async def add_bookmark(
    bookmark: UserBookmarkRequestBody,
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> Response:
    await user_service.upsert_bookmark(user.id, bookmark.filmwork_id)
    return Response(status_code=HTTPStatus.CREATED)


@router.delete("/bookmarks")
async def delete_bookmark(
    bookmark: UserBookmarkRequestBody,
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> Response:
    await user_service.delete_bookmark(user.id, bookmark.filmwork_id)
    return Response(status_code=HTTPStatus.NO_CONTENT)
