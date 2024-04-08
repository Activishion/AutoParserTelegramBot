from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine


engine: AsyncEngine = create_async_engine(settings.database_url_postgresql)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
