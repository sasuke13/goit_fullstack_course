import asyncio

from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.task import Task
from app.models.user import User
from sqlalchemy import select


async def init_db() -> None:
    """Recreate tables and seed deterministic demo data."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        session.add_all(
            [
                User(email="alice@example.com", full_name="Alice Johnson", age=28),
                User(email="bob@example.com", full_name="Bob Smith", age=31),
            ],
        )
        await session.commit()

        users = (await session.scalars(select(User).order_by(User.id))).all()
        session.add_all(
            [
                Task(title="Prepare API demo", owner_id=users[0].id),
                Task(title="Write deployment notes", owner_id=users[1].id),
            ],
        )
        await session.commit()

    print("Database initialized with demo data.")


if __name__ == "__main__":
    asyncio.run(init_db())
