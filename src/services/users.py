from fastapi import HTTPException, status

from api.auth.jwt_utils import create_access_token, create_refresh_token
from api.auth.yandex_auth import YandexAuth
from core.config import settings
from models import User
from utils.unit_of_work import BaseUnitOfWork
from schemes import Token


class UserService:
    """
    Служба для работы с пользователями.
    """

    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow
        self.authenticator = YandexAuth()

    async def get_auth_url(self):
        """
        Получение url для получения кода авторизации.

        :return: url для получения кода авторизации
        """

        authentificator = YandexAuth()
        url = await authentificator.get_auth_url()
        return url

    async def authenticate(self, code: str):
        """
        Аутентификация пользователя.

        :param code: код авторизации
        :return: данные пользователя
        """

        async with self.uow:
            authentificator = YandexAuth()
            token = await authentificator.get_auth_token(code)
            user_info = await authentificator.get_user_info(token)
            email = user_info.get("emails")[0]
            user = await self.uow.users.get_or_create(email)
            await self.uow.commit()
            return user

    async def login(self, code: str) -> tuple[Token, str]:
        """
        Вход пользователя в систему.

        :param code: код для авторизации через Yandex ID
        :return: acceess и refresh токены
        """

        user: User = await self.authenticate(code)

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        return (
            Token(
                access_token=access_token,
                token_type="Bearer",
            ),
            refresh_token,
        )

    async def refresh_access_token(self, payload: dict) -> str:
        """
        Обновление access токена.

        :param payload: словарь с данными refresh токена
        :return: acceess токен
        """

        if (
            payload.get(settings.AUTH_JWT.token_type_field)
            != settings.AUTH_JWT.refresh_token_type
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token type",
            )
        email: str = payload.get("email")
        async with self.uow:
            user = await self.uow.users.get_user_by_email(email)
            if user:
                access_token = create_access_token(user)
                return Token(
                    access_token=access_token,
                    token_type="Bearer",
                )
