from typing import List
from uuid import UUID

from pydantic import BaseModel
from beanie import Document


class AuthenticatedUser(BaseModel):
    id: UUID
    roles: List[str]


class User(Document):
    id: UUID  # type: ignore[assignment]
    bookmarks: List[UUID]

    class Settings:  # noqa: WPS431
        name = "users"
