from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.base import Base
from models.user import User  # noqa: F401 - import registers model with Base.metadata

DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        yield session
