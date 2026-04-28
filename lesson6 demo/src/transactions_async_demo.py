import asyncio

from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner: Mapped[str] = mapped_column(String(50), nullable=False)
    balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


async def main():
    engine = create_async_engine("sqlite+aiosqlite:///tx_async_demo.db", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        try:
            async with session.begin():
                session.add(Account(owner="Den", balance=150))
            print("Async transaction committed")
        except Exception as err:
            await session.rollback()
            print(f"Async transaction rolled back: {err}")


if __name__ == "__main__":
    asyncio.run(main())
