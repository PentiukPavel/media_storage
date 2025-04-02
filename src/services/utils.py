import shutil

from fastapi import UploadFile

from core.config import settings
from utils.unit_of_work import UnitOfWork


async def create_file(uow: UnitOfWork, file: UploadFile, data: dict):
    path = (
        settings.STORAGE_LOCATION
        + f"users/{data["owner_id"]}/"
        + data["filename"]
    )
    async with open(path, "wb") as media_file:
        shutil.copyfileobj(file.file, media_file)
        media_file_id = await uow.media.create_media_file(data)
        return media_file_id
