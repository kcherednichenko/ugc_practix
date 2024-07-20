from typing import List
from uuid import UUID

from beanie import Document


class FilmworkScore(Document):
    id: UUID
    score: int


class Filmwork(Document):
    id: UUID
    scores: List[FilmworkScore]

    class Settings:
        name = "filmworks"
