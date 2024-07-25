import datetime
from typing import List
from uuid import UUID

from beanie.odm.operators.find.array import ElemMatch
from beanie.operators import AddToSet, Pull

from models.filmworks import Filmwork, FilmworkScore, FilmworkReview


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

    async def get_reviews(self, filmwork_id: UUID, order: str | None) -> List:
        if order == "created_at":
            sorted_reviews = (
                await Filmwork.find(Filmwork.id == filmwork_id)
                .aggregate(
                    [
                        {"$unwind": "$reviews"},
                        {"$sort": {"reviews.created_at": -1}},
                        {"$project": {"reviews": "$reviews", "_id": 0, "id": "$reviews._id"}},
                    ],
                )
                .to_list()
            )
            sorted_reviews = [FilmworkReview(**review["reviews"]) for review in sorted_reviews]

        else:
            sorted_reviews = (
                await Filmwork.find(Filmwork.id == filmwork_id)
                .aggregate(
                    [
                        {"$unwind": "$reviews"},
                        {"$project": {"reviews": "$reviews", "_id": 0, "id": "$reviews._id"}},
                    ],
                )
                .to_list()
            )
            sorted_reviews = [FilmworkReview(**review["reviews"]) for review in sorted_reviews]

        return sorted_reviews

    async def upsert_review(self, filmwork_id: UUID, user_id: UUID, title: str, text: str) -> None:
        if not await self._has_review(filmwork_id, user_id):
            await self._insert_review(filmwork_id, user_id, title, text)
        else:
            await self._update_review(filmwork_id, user_id, title, text)

    async def delete_review(self, filmwork_id: UUID, user_id: UUID) -> None:
        await Filmwork.find_one(Filmwork.id == filmwork_id).update(
            Pull({Filmwork.reviews: {FilmworkReview.id: user_id}}),
        )

    async def like_review(self, filmwork_id: UUID, user_id: UUID, user_id_from_token: UUID) -> None:
        return await Filmwork.find_one(
            Filmwork.id == filmwork_id, ElemMatch(Filmwork.reviews, {"_id": user_id})
        ).update({"$addToSet": {"reviews.$[x].likes": user_id_from_token}}, array_filters=[{"x._id": user_id}])

    async def delete_review_like(self, filmwork_id: UUID, user_id: UUID, user_id_from_token: UUID) -> None:
        await (
            Filmwork.find_one(
                Filmwork.id == filmwork_id,
                ElemMatch(Filmwork.reviews, {"_id": user_id})
            ).update({"$pull": {"reviews.$[x].likes": user_id_from_token}}, array_filters=[{"x._id": user_id}])
        )

    async def _filmwork_already_scored_by_user(self, filmwork_id: UUID, user_id: UUID) -> bool:
        return await Filmwork.find({"_id": filmwork_id, "scores._id": user_id}).first_or_none() is not None

    async def _insert_filmwork_score(self, filmwork_id: UUID, user_id: UUID, score: int) -> None:
        filmwork_score = FilmworkScore(id=user_id, score=score)
        await Filmwork.find_one(Filmwork.id == filmwork_id).upsert(
            AddToSet({Filmwork.scores: filmwork_score}),
            on_insert=Filmwork(id=filmwork_id, scores=[filmwork_score], reviews=[]),
        )

    async def _update_filmwork_score(self, filmwork_id: UUID, user_id: UUID, score: int) -> None:
        await Filmwork.find(
            {"_id": filmwork_id, "scores._id": user_id}
        ).update({"$set": {"scores.$.score": score}})

    async def _has_review(self, filmwork_id: UUID, user_id: UUID) -> bool:
        return await Filmwork.find({"_id": filmwork_id, "reviews._id": user_id}).first_or_none() is not None

    async def _insert_review(self, filmwork_id: UUID, user_id: UUID, title: str, text: str) -> None:
        filmwork_review = FilmworkReview(
            id=user_id, title=title, text=text, created_at=datetime.datetime.now(), likes=[]
        )
        await Filmwork.find_one(Filmwork.id == filmwork_id).upsert(
            AddToSet({Filmwork.reviews: filmwork_review}),
            on_insert=Filmwork(id=filmwork_id, reviews=[filmwork_review], scores=[]),
        )

    async def _update_review(self, filmwork_id: UUID, user_id: UUID, title: str, text: str) -> None:
        await Filmwork.find({"_id": filmwork_id, "reviews._id": user_id}).update(
            {"$set": {"reviews.$.title": title, "reviews.$.text": text}}
        )


def get_filmwork_service() -> FilmworkService:
    return FilmworkService()
