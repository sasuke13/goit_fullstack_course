from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, Table

from src.db.models.base import Base

note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("note_id", "tag_id"),
)
