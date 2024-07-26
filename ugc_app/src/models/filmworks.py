from datetime import datetime
from typing import List
from uuid import UUID

from beanie import Document
from pydantic import Field, ConfigDict


class FilmworkScore(Document):
    id: UUID  # type: ignore[assignment]
    score: int


class FilmworkReview(Document):
    id: UUID  # type: ignore[assignment]
    title: str
    text: str
    created_at: datetime
    likes: List[UUID]

    model_config = ConfigDict(from_attributes=True)


class Filmwork(Document):
    id: UUID  # type: ignore[assignment]
    scores: List[FilmworkScore] = Field(default_factory=list)
    reviews: List[FilmworkReview] = Field(default_factory=list)

    class Settings:  # noqa: WPS431
        name = "filmworks"
