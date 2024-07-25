from datetime import datetime
from typing import List
from uuid import UUID

from beanie import Document


class FilmworkScore(Document):
    id: UUID  # type: ignore[assignment]
    score: int


class FilmworkReview(Document):
    id: UUID  # type: ignore[assignment]
    title: str
    text: str
    created_at: datetime
    likes: List[UUID]

    class Config:
        from_attributes = True


class Filmwork(Document):
    id: UUID  # type: ignore[assignment]
    scores: List[FilmworkScore]
    reviews: List[FilmworkReview]

    class Settings:  # noqa: WPS431
        name = "filmworks"
