from models import User
from utils.unit_of_work import BaseUnitOfWork
from schemes import MediaFileCreate
from services.utils import create_file


class MediaFilesService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def get_files_of_user(self, user_id: int):
        async with self.uow:
            media_files = await self.uow.media.get_files_of_user(user_id)
            return media_files

    async def create_media_file(
        self,
        media_file: MediaFileCreate,
        current_user: User,
        file,
    ):
        data = media_file.model_dump()
        data["owner_id"] = current_user.id
        media_file_id = await create_file(
            uow=self.uow,
            file=file,
            data=data,
        )
        await self.uow.commit()
        return media_file_id
