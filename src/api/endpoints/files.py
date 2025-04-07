from typing import Annotated, List

from fastapi import APIRouter, File, HTTPException, status, UploadFile

from api.dependencies import current_user_dep, media_service_dep
from exceptions import FilenameExists
from schemes import MediaFileRetrieve

media_v1_router = APIRouter(prefix="/media", tags=["Media"])


@media_v1_router.get(
    "/get_files/{user_id}/",
    response_model=List[MediaFileRetrieve],
    summary="Получение списка файлов.",
    description="Получение списка файлов пользователя.",
)
async def get_files_of_user_endpoint(
    media_service: media_service_dep, user_id: int
):
    return await media_service.get_files_of_user(user_id)


@media_v1_router.post(
    "/add_file/{filename}/",
    summary="Добавление файла.",
    description="Добавление файла.",
    response_model=MediaFileRetrieve,
)
async def create_media_file_endpoint(
    filename: str,
    file: Annotated[UploadFile, File(description="Фото к услуге")],
    media_service: media_service_dep,
    current_user: current_user_dep,
):
    try:
        return await media_service.create_media_file(
            filename=filename,
            current_user=current_user,
            file=file,
        )
    except FilenameExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
