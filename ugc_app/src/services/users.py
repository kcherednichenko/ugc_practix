import datetime
from typing import List
from uuid import UUID
import logging

from beanie.odm.operators.find.array import ElemMatch
from beanie.operators import AddToSet, Pull

from models.users import User, UserReview

logger = logging.getLogger(__name__)


class UserService:
    async def get_bookmarks(self, user_id: UUID) -> List[UUID]:
        logger.info("Getting bookmarks for user %s", user_id)
        user = await User.find_one(User.id == user_id)
        return user.bookmarks if user else []

    async def upsert_bookmark(self, user_id: UUID, filmwork_id: UUID) -> None:
        logger.info("Upserting bookmark %s for user %s", filmwork_id, user_id)
        await User.find_one(User.id == user_id).upsert(
            AddToSet({User.bookmarks: filmwork_id}),
            on_insert=User(id=user_id, bookmarks=[filmwork_id]),
        )

    async def delete_bookmark(self, user_id: UUID, filmwork_id: UUID) -> None:
        logger.info("Deleting bookmark %s for user %s", filmwork_id, user_id)
        await User.find_one(User.id == user_id).update(
            Pull({User.bookmarks: filmwork_id}),
        )

    async def upsert_review(self, filmwork_id: UUID, user_id: UUID, title: str, text: str) -> None:
        if not await self._has_review(filmwork_id, user_id):
            await self._insert_review(filmwork_id, user_id, title, text)
        else:
            await self._update_review(filmwork_id, user_id, title, text)

    async def delete_review(self, filmwork_id: UUID, user_id: UUID) -> None:
        await User.find_one(User.id == user_id).update(
            Pull({User.reviews: {UserReview.id: filmwork_id}}),
        )

    async def get_reviews(self, user_id: UUID) -> List[UserReview]:
        user = await User.find_one(User.id == user_id)
        return user.reviews if user else []

    async def like_review(self, filmwork_id: UUID, user_id: UUID, user_id_from_token: UUID) -> None:
        await User.find_one(
            User.id == user_id,
            ElemMatch(User.reviews, {"_id": filmwork_id})
        ).update(
            {"$addToSet": {"reviews.$[x].likes": user_id_from_token}}, array_filters=[{"x._id": filmwork_id}]
        )

    async def delete_review_like(self, filmwork_id: UUID, user_id: UUID, user_id_from_token: UUID) -> None:
        await User.find_one(
            User.id == user_id,
            ElemMatch(User.reviews, {"_id": filmwork_id})
        ).update(
            {"$pull": {"reviews.$[x].likes": user_id_from_token}}, array_filters=[{"x._id": filmwork_id}]
        )

    async def _has_review(self, filmwork_id: UUID, user_id: UUID) -> bool:
        return await User.find({"_id": user_id, "reviews._id": filmwork_id}).first_or_none() is not None

    async def _insert_review(self, filmwork_id: UUID, user_id: UUID, title: str, text: str) -> None:
        user_review = UserReview(
            id=filmwork_id,
            title=title,
            text=text,
            created_at=datetime.datetime.now(),
            likes=[]
        )
        await User.find_one(User.id == user_id).upsert(
            AddToSet({User.reviews: user_review}),
            on_insert=User(id=user_id, reviews=[user_review]),
        )

    async def _update_review(self, filmwork_id: UUID, user_id: UUID, title: str, text: str) -> None:
        await User.find({"_id": user_id, "reviews._id": filmwork_id}).update(
            {"$set": {"reviews.$.title": title, "reviews.$.text": text}}
        )


def get_user_service() -> UserService:
    return UserService()
