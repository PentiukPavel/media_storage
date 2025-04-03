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
    payload = {settings.AUTH_JWT.token_type_field: token_type}
    payload.update(token_data)
    return encode_jwt(
        payload=payload,
        delta_minutes=delta_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: User) -> str:
    payload = {"email": user.email}
    return create_jwt(
        token_type=settings.AUTH_JWT.access_token_type,
        token_data=payload,
        delta_minutes=settings.AUTH_JWT.access_token_lifetime,
    )


def create_refresh_token(user: User) -> str:
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
