from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, status, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
import jwt
from jwt.exceptions import InvalidTokenError

from core.config import settings
from models import User
from utils.unit_of_work import UnitOfWork


http_bearer = HTTPBearer()


def encode_jwt(
    payload: dict,
    private_key: str = settings.AUTH_JWT.private_key_path.read_text(),
    algorithm: str = settings.AUTH_JWT.algorithm,
    delta_minutes: int = settings.AUTH_JWT.access_token_lifetime,
    expire_timedelta: timedelta | None = None,
) -> str:
    payload_upd = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=delta_minutes)
    payload_upd.update(exp=expire, iat=now)
    encoded = jwt.encode(payload, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.AUTH_JWT.public_key_path.read_text(),
    algorithm: str = settings.AUTH_JWT.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    binary_pswd = bcrypt.hashpw(pwd_bytes, salt)
    return binary_pswd.decode("ascii")


def validate_password(password: str, hashed_password: str) -> bool:
    binary_pswd = hashed_password.encode("ascii")
    return bcrypt.checkpw(password.encode(), binary_pswd)


def get_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )


async def current_user(
    payload: dict = Depends(get_payload),
) -> User:
    if (
        payload.get(settings.AUTH_JWT.token_type_field)
        != settings.AUTH_JWT.access_token_type
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token type",
        )
    email: str = payload.get("sub")
    uow = UnitOfWork()
    async with uow:
        user = await uow.users.get_user_by_email(email)
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )
