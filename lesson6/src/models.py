
from datetime import datetime
from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from sqlalchemy import (
    DateTime,
    String,
    Integer,
    Boolean,
    ForeignKey,
    Table,
    Column,
)


class Base(DeclarativeBase):
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False, default=18)

    notes: Mapped[List["Note"]] = relationship("Note", back_populates="user", cascade="all, delete-orphan")

    @validates("age")
    def validate_age(self, key, age):
        if age < 18:
            raise ValueError("Age must be greater than 18")
        return age


class Note(Base):
    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(String(60), nullable=False)
    user_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="notes")
    records: Mapped[List["Record"]] = relationship("Record", back_populates="note", cascade="all, delete-orphan")


class Record(Base):
    __tablename__ = "records"

    name: Mapped[str] = mapped_column(String(60), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)

    note_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("notes.id"), nullable=False)

    note: Mapped["Note"] = relationship("Note", back_populates="records")


class Tag(Base):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)


# async def main():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
    
#     async with async_session() as session:
#         user = User(username="test1", age=17, notes=[Note(title="test")])
#         session.add(user)
#         await session.commit()


# if __name__ == "__main__":
#     asyncio.run(main())
