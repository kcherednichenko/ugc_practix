from typing import List
from uuid import UUID

from pydantic import BaseModel, ValidationError
import jwt

from settings import settings
from models.users import User

_ALGORITHM = "RS256"


def get_user_from_token(token: str) -> User | None:
    try:
        payload = _decode_token(token)
    except (jwt.exceptions.InvalidTokenError, ValidationError) as e:
        return None
    return User(id=payload.user_id, roles=payload.roles)


def _decode_token(token: str) -> "_TokenPayload":
    return _TokenPayload(**jwt.decode(token, settings.jwt_public_key, algorithms=[_ALGORITHM]))


class _TokenPayload(BaseModel):
    user_id: UUID
    roles: List[str]
