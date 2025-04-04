from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Cookie, Depends, status, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from core.config import settings


http_bearer = HTTPBearer()


def encode_jwt(
    payload: dict,
    private_key: str = settings.AUTH_JWT.private_key_path.read_text(),
    algorithm: str = settings.AUTH_JWT.algorithm,
    delta_minutes: int = settings.AUTH_JWT.access_token_lifetime,
    expire_timedelta: timedelta | None = None,
) -> str:
    """
    Кодирование JWT токена.

    :param payload: данные токена
    :param private_key: приватный ключ для кодирования
    :param algorithm: тип алгоритма кодирования
    :param delta_minutes: срок действия токена в минутах
    :param expire_timedelta: срок действия токена - тип timedelta (опционально)
    :return: JWT токен
    """

    payload_upd = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=delta_minutes)
    payload_upd.update(exp=expire, iat=now)
    encoded = jwt.encode(payload_upd, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.AUTH_JWT.public_key_path.read_text(),
    algorithm: str = settings.AUTH_JWT.algorithm,
) -> dict:
    """
    Декодирование JWT токена.

    :param token: JWT токен
    :param public_key: публичный ключ для кодирования
    :param algorithm: тип алгоритма кодирования
    :return: данные зашифрованные в токене
    """

    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> str:
    """
    Хеширование пароля.

    :param password: пароль в исходном виде
    :return: хеш пароля
    """

    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    binary_pswd = bcrypt.hashpw(pwd_bytes, salt)
    return binary_pswd.decode("ascii")


def validate_password(password: str, hashed_password: str) -> bool:
    """
    Валидация пароля.

    :param password: пароль в исходном виде
    :param hashed_password: хеш пароля
    :return: совпадение
    """

    binary_pswd = hashed_password.encode("ascii")
    return bcrypt.checkpw(password.encode(), binary_pswd)


def get_access_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    """
    Получение данных пользователя из request.

    :param credentials: данные из request
    :return: данные пользователя
    """

    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def get_refresh_payload(refresh_token: str = Cookie(None)) -> dict:
    """
    Получение данных пользователя из cookie.
    :param token: данные из request
    :return: данные пользователя
    """

    print(refresh_token)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing",
        )
    try:
        payload = decode_jwt(refresh_token)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
