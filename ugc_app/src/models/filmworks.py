from typing import List
from uuid import UUID

from beanie import Document


class FilmworkScore(Document):
    id: UUID  # type: ignore[assignment]
    score: int


class Filmwork(Document):
    id: UUID  # type: ignore[assignment]
    scores: List[FilmworkScore]

    class Settings:  # noqa: WPS431
        name = "filmworks"
