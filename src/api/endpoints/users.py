from fastapi import APIRouter, Depends

from api.dependencies import users_service_dep, current_user_dep
from api.auth.utils import get_access_payload
from schemes import Code, Token, UserRetrieve

users_v1_router = APIRouter(prefix="/users", tags=["Users"])


@users_v1_router.get(
    "/get_auth_code/",
    summary="URL для получения кода.",
    description="Получение url для получения кода авторизации.",
)
async def get_auth_code_endpoint(
    users_service: users_service_dep,
):
    return await users_service.get_auth_code()


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
async def login_endpoint(users_service: users_service_dep, code: Code):
    return await users_service.login(code)


@users_v1_router.get(
    "/refresh/",
    response_model=Token,
    summary="Обновление access токена.",
    description="Обновление access токена через refresh токен.",
)
async def refresh_token_endpoint(
    users_service: users_service_dep,
    payload: dict = Depends(get_access_payload),
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
