from fastapi import Depends, status, HTTPException

from api.auth.utils import get_access_payload
from core.config import settings
from utils.unit_of_work import UnitOfWork
from schemes import UserRetrieve


async def current_user(
    payload: dict = Depends(get_access_payload),
) -> UserRetrieve:
    """
    Получение данных пользоватееля.

    :return: данных пользоватееля
    """

    if (
        payload.get(settings.AUTH_JWT.token_type_field)
        != settings.AUTH_JWT.access_token_type
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token type",
        )
    email: str = payload.get("email")
    uow = UnitOfWork()
    async with uow:
        user = await uow.users.get_user_by_email(email)
        if user:
            return user.to_read_model()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )
