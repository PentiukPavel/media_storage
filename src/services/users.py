from fastapi import Depends, status, HTTPException
from fastapi.security import (
    HTTPBearer,
)

from api.auth.helpers import create_access_token, create_refresh_token
from api.auth.yandex_auth import YandexAuth
from api.auth.utils import get_payload
from core.config import settings
from models import User
from utils.unit_of_work import BaseUnitOfWork
from schemes import Token

http_bearer = HTTPBearer()


class UserService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow
        self.authenticator = YandexAuth()

    async def get_auth_code(self):
        authentificator = YandexAuth()
        url = await authentificator.get_auth_code()
        return url

    async def authenticate(self, code: str):
        async with self.uow:
            authentificator = YandexAuth()
            token = await authentificator.get_auth_token(code)
            user_info = await authentificator.get_user_info(token)
            email = user_info.get("emails")[0]
            user = await self.uow.users.get_or_create(email)
            await self.uow.commit()
            return user

    async def login(self, code: str):
        user: User = await self.authenticate(code)

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    async def refresh_access_token(
        self,
        payload: dict = Depends(get_payload),
    ) -> str:
        if (
            payload.get(settings.AUTH_JWT.token_type_field)
            != settings.AUTH_JWT.refresh_token_type
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token type",
            )
        email: str = payload.get("sub")
        async with self.uow:
            user = await self.uow.users.get_user_by_email(email)
            if user:
                access_token = create_access_token(user)
                return Token(
                    access_token=access_token,
                    token_type="Bearer",
                )
