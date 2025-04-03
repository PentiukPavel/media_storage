from pathlib import Path

import shutil

from fastapi import UploadFile

from core.config import settings
from models import User
from utils.unit_of_work import BaseUnitOfWork


class MediaFilesService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def get_files_of_user(self, user_id: int):
        async with self.uow:
            media_files = await self.uow.media.get_files_of_user(user_id)
            return media_files

    async def create_media_file(
        self,
        filename: str,
        current_user: User,
        file: UploadFile,
    ):
        data = {
            "filename": filename,
            "owner_id": current_user.id,
        }
        filename = file.filename
        ext = filename.split(".")[-1]
        path = Path(
            settings.STORAGE_LOCATION,
            f"{data["owner_id"]}",
            f"{data["filename"]}.{ext}\\",
        )
        data["file_url"] = str(path)
        async with open(path, "wb+") as media_file:
            shutil.copyfileobj(file.file, media_file)
        async with self.uow:
            media_file = await self.uow.media.create_media_file(data)
            await self.uow.commit()
        return media_file
