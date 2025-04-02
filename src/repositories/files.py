from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import MedeaFile
from repositories.base import AbstrsctRepository


class MediaFilesRepository(AbstrsctRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_files_of_user(self, user_id: int) -> List[MedeaFile]:
        query = select(MedeaFile).where(MedeaFile.owner_id == user_id)
        result = await self.session.execute(query)
        files = [row[0].to_read_model() for row in result]
        return files

    async def create_media_file(self, data: dict) -> int:
        media_file = MedeaFile(**data)
        self.session.add(media_file)
        await self.session.flush()
        await self.session.refresh(media_file)
        return media_file.id
