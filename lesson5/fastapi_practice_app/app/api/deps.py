from collections.abc import AsyncGenerator

from app.core.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession


async def db_session_dep() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides an async DB session."""
    async for session in get_db_session():
        yield session
