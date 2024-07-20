from typing import Annotated
from http import HTTPStatus

from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.users import User
from services.tokens import get_user_from_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid authorization code")
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Only Bearer token might be accepted")
        return credentials.credentials


security_jwt = JWTBearer()


def get_authenticated_user(
    token: Annotated[str, Depends(security_jwt)],
) -> User:
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    return user
