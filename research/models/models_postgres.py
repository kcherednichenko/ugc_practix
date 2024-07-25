import uuid
import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID

from .base_model import OrmBase
from sqlalchemy import DateTime


class Filmwork(OrmBase):
    __tablename__ = "Filmwork"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                     unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'<Filmwork {self.id}>'


class Scores(OrmBase):
    __tablename__ = "Scores"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                     unique=True, nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    filmwork_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=False, nullable=False)
    score: Mapped[int] = mapped_column(default=0, nullable=False)

    def __repr__(self) -> str:
        return f'<Scores {self.id}>'


class Reviews(OrmBase):
    __tablename__ = "Reviews"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                     unique=True, nullable=False)
    filmwork_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    header: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    text: Mapped[str] = mapped_column(String(3000), unique=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=None)

    def __repr__(self) -> str:
        return f'<Reviews {self.id}>'


class ReviewsUser(OrmBase):
    __tablename__ = "ReviewsUser"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                     unique=True, nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    reviews_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'<ReviewsUser {self.id}>'


class LikeReviews(OrmBase):
    __tablename__ = "LikeReviews"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                     unique=True, nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4,
                                          unique=True, nullable=False)
    reviews_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4,
                                             unique=True, nullable=False)
    like: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f'<LikeReviews {self.id}>'


class User(OrmBase):
    __tablename__ = "User"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                     unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'<User {self.id}>'


class Bookmarks(OrmBase):
    __tablename__ = "Bookmarks"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                     unique=True, nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    filmwork_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'<Bookmarks {self.id}>'
