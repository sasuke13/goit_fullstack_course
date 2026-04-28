import asyncio

from sqlalchemy import Integer, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AsyncBase(DeclarativeBase):
    pass


class AsyncUser(AsyncBase):
    __tablename__ = "async_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)


async def main():
    engine = create_async_engine("sqlite+aiosqlite:///async_demo.db", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(AsyncBase.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        session.add(AsyncUser(username="Charlie"))
        await session.commit()

        result = await session.execute(select(AsyncUser))
        users = result.scalars().all()
        print([u.username for u in users])


if __name__ == "__main__":
    asyncio.run(main())
