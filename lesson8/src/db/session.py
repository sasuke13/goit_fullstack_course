import contextlib
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from src.settings import settings


class DatabaseSessionManager:
    def __init__(self, db_url: str):
        self._engine: AsyncEngine = create_async_engine(db_url)
        self._session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
        )

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


session_manager = DatabaseSessionManager(settings.DB_URL)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session
