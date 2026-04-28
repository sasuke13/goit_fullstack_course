from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from src.db.models.associations import note_m2m_tag
from src.db.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


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
    async def get_by_id(cls, session: AsyncSession, note_id: int) -> "Note":
        stmt = select(cls).options(selectinload(cls.tags)).filter_by(id=note_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
