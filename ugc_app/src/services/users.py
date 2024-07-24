from typing import List
from uuid import UUID
import logging

from beanie.operators import AddToSet, Pull

from models.users import User

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


def get_user_service() -> UserService:
    return UserService()
