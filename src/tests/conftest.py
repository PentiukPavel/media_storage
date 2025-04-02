import asyncio

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import NullPool

from core.database import Base, get_async_session
from core.config import DATABASE_URL_TEST
from main import app


@pytest_asyncio.fixture(autouse=True, scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope="function")
async def get_engine():
    engine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        yield conn
        await conn.close()


@pytest_asyncio.fixture(autouse=True, scope="function")
async def get_session(get_engine):
    engine_test = get_engine
    async_session_maker = sessionmaker(
        engine_test, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def async_client(get_session):
    app.dependency_overrides[get_async_session] = lambda: get_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
