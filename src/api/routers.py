from fastapi import APIRouter

from api.endpoints.users import users_v1_router
from api.endpoints.files import media_v1_router


v1_main_router = APIRouter(prefix="/api")
v1_main_router.include_router(media_v1_router)
v1_main_router.include_router(users_v1_router)
