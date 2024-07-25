from uuid import UUID

from beanie.operators import AddToSet, Pull

from models.filmworks import Filmwork, FilmworkScore


class FilmworkService:
    async def get_average_score(self, filmwork_id: UUID) -> float | None:
        avg_score_field_name = "avg_score"
        avg_result = (
            await Filmwork.find(Filmwork.id == filmwork_id)
            .aggregate(
                [
                    {"$unwind": "$scores"},
                    {
                        "$group": {
                            "_id": None,
                            avg_score_field_name: {"$avg": "$scores.score"},
                        },
                    },
                ],
            )
            .to_list()
        )
        return (avg_result or [{}])[0].get(avg_score_field_name)

    async def upsert_user_score(self, filmwork_id: UUID, user_id: UUID, score: int) -> None:
        if not await self._filmwork_already_scored_by_user(filmwork_id, user_id):
            await self._insert_filmwork_score(filmwork_id, user_id, score)
        else:
            await self._update_filmwork_score(filmwork_id, user_id, score)

    async def delete_user_score(self, filmwork_id: UUID, user_id: UUID) -> None:
        await Filmwork.find_one(Filmwork.id == filmwork_id).update(
            Pull({Filmwork.scores: {FilmworkScore.id: user_id}}),
        )

    async def _filmwork_already_scored_by_user(self, filmwork_id: UUID, user_id: UUID) -> bool:
        return await Filmwork.find({"_id": filmwork_id, "scores._id": user_id}).first_or_none() is not None

    async def _insert_filmwork_score(self, filmwork_id: UUID, user_id: UUID, score: int) -> None:
        filmwork_score = FilmworkScore(id=user_id, score=score)
        await Filmwork.find_one(Filmwork.id == filmwork_id).upsert(
            AddToSet({Filmwork.scores: filmwork_score}),
            on_insert=Filmwork(id=filmwork_id, scores=[filmwork_score]),
        )

    async def _update_filmwork_score(self, filmwork_id: UUID, user_id: UUID, score: int) -> None:
        await Filmwork.find({"_id": filmwork_id, "scores._id": user_id}).update(
            {"$set": {"scores.$.score": score}}
        )


def get_filmwork_service() -> FilmworkService:
    return FilmworkService()
