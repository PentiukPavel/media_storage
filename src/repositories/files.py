from typing import List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import MedeaFile
from repositories.base import AbstrsctRepository
from schemes import MediaFileRetrieve


class MediaFilesRepository(AbstrsctRepository):
    """
    SQLAlchemy репозитория для взаимодействия с таблицей файлов.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_files_of_user(self, user_id: int) -> List[MediaFileRetrieve]:
        """
        Получение списка файлов пользователя из БД.

        :param user_id: id пользователя
        :return: список файлов пользователя
        """

        query = select(MedeaFile).filter_by(owner_id=user_id)
        result = await self.session.execute(query)
        files = [row[0].to_read_model() for row in result]
        return files

    async def create_media_file(self, data: dict) -> MediaFileRetrieve:
        """
        Сохранение данных о файле в БД.

        :param data: сведения о файле
        :return: сведения о сохраненном файле
        """

        stmnt = insert(MedeaFile).values(**data).returning(MedeaFile)
        result = await self.session.execute(stmnt)
        return result.scalar_one().to_read_model()
