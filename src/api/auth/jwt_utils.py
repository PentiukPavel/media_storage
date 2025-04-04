from datetime import timedelta

from api.auth.utils import encode_jwt
from core.config import settings
from models import User


def create_jwt(
    token_type: str,
    token_data: dict,
    delta_minutes: int = settings.AUTH_JWT.access_token_lifetime,
    expire_timedelta: timedelta | None = None,
):
    """
    Создание JWT токена.

    :param token_type: тип токена
    :param token_data: данные для кодирования в токене
    :param delta_minutes: срок действия токена в минутах
    :param expire_timedelta: срок действия токена - тип timedelta (опционально)
    :return: JWT токен
    """

    payload = {settings.AUTH_JWT.token_type_field: token_type}
    payload.update(token_data)
    return encode_jwt(
        payload=payload,
        delta_minutes=delta_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: User) -> str:
    """
    Создание access JWT токена.

    :param user: данные пользователя
    :return: access JWT токен
    """

    payload = {"email": user.email}
    return create_jwt(
        token_type=settings.AUTH_JWT.access_token_type,
        token_data=payload,
        delta_minutes=settings.AUTH_JWT.access_token_lifetime,
    )


def create_refresh_token(user: User) -> str:
    """
    Создание refresh JWT токена.

    :param user: данные пользователя
    :return: refresh JWT токен
    """

    payload = {
        "email": user.email,
    }
    return create_jwt(
        token_type=settings.AUTH_JWT.refresh_token_type,
        token_data=payload,
        expire_timedelta=timedelta(
            days=settings.AUTH_JWT.refresh_token_lifetime
        ),
    )
