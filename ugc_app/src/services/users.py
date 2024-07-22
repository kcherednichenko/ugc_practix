from typing import List
from uuid import UUID

from beanie.operators import AddToSet, Pull

from models.users import User


class UserService:
    async def get_bookmarks(self, user_id: UUID) -> List[UUID]:
        user = await User.find_one(User.id == user_id)
        return user.bookmarks if user else []

    async def upsert_bookmark(self, user_id: UUID, filmwork_id: UUID) -> None:
        await User.find_one(User.id == user_id).upsert(
            AddToSet({User.bookmarks: filmwork_id}),
            on_insert=User(id=user_id, bookmarks=[filmwork_id]),
        )

    async def delete_bookmark(self, user_id: UUID, filmwork_id: UUID) -> None:
        await User.find_one(User.id == user_id).update(
            Pull({User.bookmarks: filmwork_id}),
        )


def get_user_service() -> UserService:
    return UserService()
