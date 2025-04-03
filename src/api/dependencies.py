from typing import Annotated, Dict

from fastapi import Depends

from api.auth.utils import get_payload
from api.auth.db_utils import current_user
from models import User
from services import MediaFilesService, UserService
from utils.unit_of_work import BaseUnitOfWork, UnitOfWork


UOWDep = Annotated[BaseUnitOfWork, Depends(UnitOfWork)]


def get_users_service(uow: UOWDep) -> UserService:
    return UserService(uow)


def get_media_service(uow: UOWDep) -> MediaFilesService:
    return MediaFilesService(uow)


users_service_dep = Annotated[UserService, Depends(get_users_service)]
media_service_dep = Annotated[MediaFilesService, Depends(get_media_service)]
current_user_dep = Annotated[User, Depends(current_user)]
payload_dep = Annotated[Dict, Depends(get_payload)]
