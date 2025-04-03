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
    encoded = jwt.encode(payload_upd, private_key, algorithm)
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
