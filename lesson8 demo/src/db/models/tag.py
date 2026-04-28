from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.associations import note_m2m_tag
from src.db.models.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)
    notes: Mapped[list["Note"]] = relationship(
        "Note", secondary=note_m2m_tag, back_populates="tags"
    )
