from pathlib import Path
import shutil

from fastapi import UploadFile

from core.config import settings
from utils.unit_of_work import UnitOfWork


async def create_file(uow: UnitOfWork, file: UploadFile, data: dict):
    filename = file.filename
    ext = filename.split(".")[-1]
    path = Path(
        settings.STORAGE_LOCATION,
        f"{data["owner_id"]}",
        f"{data["filename"]}.{ext}",
    )
    async with open(path, "wb") as media_file:
        shutil.copyfileobj(file.file, media_file)
        media_file_id = await uow.media.create_media_file(data)
        return media_file_id
