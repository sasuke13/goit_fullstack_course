from __future__ import annotations

from typing import List, Optional

from sqlalchemy import Column, ForeignKey, String, Table, func, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pathlib import Path


# db_path = Path(__file__).resolve().parent.parent / "data" / "practice.db"
# engine = create_engine(f"sqlite+pysqlite:///{db_path}", echo=True, future=True)


class Base(DeclarativeBase):
    pass


student_course = Table(
    "student_course",
    Base.metadata,
    Column(
        "student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("course_id", ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False, index=True
    )
    age: Mapped[Optional[int]]
    created_at: Mapped[str] = mapped_column(server_default=func.current_timestamp())

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    profile: Mapped[Optional["Profile"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username!r}, email={self.email!r})"


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    street: Mapped[str] = mapped_column(String(150), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id}, city={self.city!r}, street={self.street!r})"


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"Profile(id={self.id}, user_id={self.user_id}, bio={self.bio!r})"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)

    courses: Mapped[List["Course"]] = relationship(
        secondary=student_course,
        back_populates="students",
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id}, full_name={self.full_name!r})"


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    students: Mapped[List[Student]] = relationship(
        secondary=student_course,
        back_populates="courses",
    )

    def __repr__(self) -> str:
        return f"Course(id={self.id}, title={self.title!r})"


# Base.metadata.create_all(engine)

