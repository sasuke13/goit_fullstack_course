from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.associations import note_m2m_tag
from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.tag import Tag


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=note_m2m_tag, back_populates="notes"
    )

    @classmethod
    async def get_all(
        cls, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list["Note"]:
        stmt = select(cls).options(selectinload(cls.tags)).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def count_all(cls, session: AsyncSession) -> int:
        stmt = select(func.count(cls.id))
        result = await session.execute(stmt)
        return int(result.scalar_one())

    @classmethod
    async def get_by_id(cls, session: AsyncSession, note_id: int) -> "Note | None":
        stmt = select(cls).options(selectinload(cls.tags)).filter_by(id=note_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def create(
        cls, session: AsyncSession, payload: dict, tags: list["Tag"]
    ) -> "Note":
        note = cls(**payload, tags=tags)
        session.add(note)
        await session.commit()
        await session.refresh(note)
        refreshed = await cls.get_by_id(session, note.id)
        if refreshed is None:
            raise RuntimeError("Created note not found after refresh")
        return refreshed

    async def update(
        self, session: AsyncSession, payload: dict, tags: list["Tag"]
    ) -> "Note":
        for key, value in payload.items():
            setattr(self, key, value)
        self.tags = tags
        await session.commit()
        await session.refresh(self)
        refreshed = await self.__class__.get_by_id(session, self.id)
        if refreshed is None:
            raise RuntimeError("Updated note not found after refresh")
        return refreshed

    async def update_status(self, session: AsyncSession, done: bool) -> "Note":
        self.done = done
        await session.commit()
        await session.refresh(self)
        refreshed = await self.__class__.get_by_id(session, self.id)
        if refreshed is None:
            raise RuntimeError("Updated note not found after refresh")
        return refreshed

    async def remove(self, session: AsyncSession) -> None:
        await session.delete(self)
        await session.commit()
