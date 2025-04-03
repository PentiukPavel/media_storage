from models import User
from utils.unit_of_work import BaseUnitOfWork
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
        filename: str,
        current_user: User,
        file,
    ):
        data = {
            "filename": filename,
            "owner_id": current_user.id,
        }
        media_file_id = await create_file(
            uow=self.uow,
            file=file,
            data=data,
        )
        await self.uow.commit()
        return media_file_id
