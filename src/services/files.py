import os

import aiofiles

from fastapi import UploadFile

from core.config import settings
from models import User
from utils.unit_of_work import BaseUnitOfWork


class MediaFilesService:
    """
    Служба для работы с файлами.
    """

    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def get_files_of_user(self, user_id: int):
        """
        Получение списка файлов пользователя.

        :param user_id: id пользователя
        :return: список файлов пользователя
        """

        async with self.uow:
            media_files = await self.uow.media.get_files_of_user(user_id)
            return media_files

    async def create_media_file(
        self,
        filename: str,
        current_user: User,
        file: UploadFile,
    ):
        """
        Загрузка файла на сервер.

        :param filename: имя файла
        :param current_user: данные пользователя
        :param file: файл
        :return: данные загруженного файла
        """

        ext = file.filename.split(".")[-1]
        path = os.path.join(
            settings.STORAGE_LOCATION,
            f"{filename}.{ext}",
        )
        data = {
            "filename": filename,
            "owner_id": current_user.id,
            "file_url": str(path),
        }
        async with aiofiles.open(path, "wb") as media_file:
            content = await file.read()
            await media_file.write(content)
        async with self.uow:
            media_file = await self.uow.media.create_media_file(data)
            await self.uow.commit()
        return media_file
