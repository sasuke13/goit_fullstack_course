from __future__ import annotations

import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db import get_async_engine, get_async_session_factory
from models import Address, Base, User


async def reset_async_db() -> None:
    engine = get_async_engine(echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def seed_async_data() -> None:
    SessionLocal = get_async_session_factory(echo=True)
    async with SessionLocal() as session:
        session.add_all(
            [
                User(
                    username="maria",
                    email="maria@example.com",
                    age=30,
                    addresses=[Address(city="Kharkiv", street="Science 11")],
                ),
                User(
                    username="oleg",
                    email="oleg@example.com",
                    age=25,
                    addresses=[Address(city="Kyiv", street="River 15")],
                ),
            ],
        )
        await session.commit()


async def run_async_queries() -> None:
    SessionLocal = get_async_session_factory(echo=True)
    async with SessionLocal() as session:
        print("\n[Async ORM] select + eager loading:")
        stmt = select(User).options(selectinload(User.addresses)).order_by(User.id)
        result = await session.scalars(stmt)
        users = result.all()
        for user in users:
            cities = ", ".join(address.city for address in user.addresses)
            print(f"- {user.username}: {cities}")


async def run_async_orm_demo() -> None:
    await reset_async_db()
    await seed_async_data()
    await run_async_queries()


if __name__ == "__main__":
    asyncio.run(run_async_orm_demo())
