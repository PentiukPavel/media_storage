from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories.base import AbstrsctRepository


class UserRepository(AbstrsctRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            data = {"email": email}
            new_user = User(**data)
            self.session.add(new_user)
            await self.session.flush()
            await self.session.refresh(new_user)
            return new_user

        return user

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        return user
