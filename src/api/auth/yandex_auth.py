import httpx
from urllib.parse import urlencode

from fastapi import HTTPException, status

from core.config import settings
from core.choices import APIExceptions
from schemes import Code


class YandexAuth:
    """
    Класс для авторизации через yandex ID.
    """

    def __init__(self):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.CLIENT_SECRET
        self.redirect_uri = settings.REDIRECT_URI

    async def get_auth_url(self) -> str:
        """
        Получение url для получения кода авторизации по Yandex ID.

        :return: url для получения кода авторизации по Yandex ID
        """

        base_url = "https://oauth.yandex.ru/authorize"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
        }
        code_url = f"{base_url}?{urlencode(params)}"
        return code_url

    async def get_auth_token(self, code: Code) -> str:
        """
        Получение токена для получения данных пользователя по Yandex ID.

        :param code: код авторизации
        :return: токен для получения данных пользователя по Yandex ID
        """

        token_url = "https://oauth.yandex.ru/token"
        code = code.model_dump()["code"]
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=APIExceptions.CAN_NOT_GET_AUTH_TOKEN.value,
                )
            tokens = response.json()
            return tokens.get("access_token")

    async def get_user_info(self, access_token: str) -> dict:
        """
        Получение данных пользователя по Yandex ID.

        :param access_token: токен
        :return: данные пользователя
        """

        user_info_url = "https://login.yandex.ru/info"
        headers = {"Authorization": f"OAuth {access_token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(user_info_url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail=APIExceptions.CAN_NOT_GET_USER_INFO.value,
                )
            return response.json()
