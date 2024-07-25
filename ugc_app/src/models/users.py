from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel
from beanie import Document


class AuthenticatedUser(BaseModel):
    id: UUID
    roles: List[str]


class UserReview(Document):
    id: UUID  # type: ignore[assignment]
    title: str
    text: str
    created_at: datetime
    likes: List[UUID]

    class Config:
        from_attributes = True


class User(Document):
    id: UUID  # type: ignore[assignment]
    bookmarks: List[UUID]
    reviews: List[UserReview]

    class Settings:  # noqa: WPS431
        name = "users"
