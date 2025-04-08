import os

import aiofiles

from fastapi import UploadFile

from core.config import settings
from core.limits import Limit
from exceptions import (
    FileIsTooLarge,
    FilenameExists,
    WrongFilename,
    WrongFileType,
)
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
        :raises FilenameExists: файл с таким именем уже существует
        :raises WrongFilename: слишком длинное имя файла
        :return: данные загруженного файла
        """

        file_size = file.file.tell()

        if file_size > Limit.MAX_FILE_SIZE_MB.value:
            raise FileIsTooLarge()

        content_type = file.content_type
        if content_type not in settings.FILE_TYPES:
            raise WrongFileType()

        if len(filename) > Limit.MAX_LENGTH_FILENAME.value:
            raise WrongFilename()

        async with self.uow:
            if (
                await self.uow.media.get_file_by_filename_and_user_id(
                    filename=filename,
                    user_id=current_user.id,
                )
                is not None
            ):
                raise FilenameExists()

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

            media_file = await self.uow.media.create_media_file(data)
            await self.uow.commit()
            return media_file
