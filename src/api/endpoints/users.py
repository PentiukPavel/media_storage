from fastapi import APIRouter, Depends, Response

from api.dependencies import users_service_dep, current_user_dep
from api.auth.utils import get_refresh_payload
from core.config import settings
from schemes import Code, Token, UserRetrieve

users_v1_router = APIRouter(prefix="/users", tags=["Users"])


@users_v1_router.get(
    "/get_auth_code/",
    summary="URL для получения кода.",
    description="Получение url для получения кода авторизации.",
)
async def get_auth_url_endpoint(
    users_service: users_service_dep,
):
    return await users_service.get_auth_url()


@users_v1_router.post(
    "/login/",
    summary="Логин.",
    description=(
        "Вход в систему через Yandex ID с помощью кода."
        "Код необходимо получить при переходе по ссылке, "
        "сгенерированной при использовании эндпоинта 'URL для получения кода.'"
    ),
    response_model_include=Token,
)
async def login_endpoint(
    response: Response,
    users_service: users_service_dep,
    code: Code,
):
    acess_token, refresh_token = await users_service.login(code)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=settings.AUTH_JWT.refresh_token_lifetime * 24 * 3600,
    )

    return acess_token


@users_v1_router.get(
    "/refresh/",
    response_model=Token,
    summary="Обновление access токена.",
    description="Обновление access токена через refresh токен.",
)
async def refresh_token_endpoint(
    users_service: users_service_dep,
    payload: dict = Depends(get_refresh_payload),
):
    return await users_service.refresh_access_token(payload)


@users_v1_router.get(
    "/me/",
    response_model=UserRetrieve,
    summary="Информация о пользователе.",
    description="Получение информации о пользователе.",
)
async def get_user_endpoint(
    current_user: current_user_dep,
):
    return current_user
