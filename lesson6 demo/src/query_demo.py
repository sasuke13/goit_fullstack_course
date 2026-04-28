from sqlalchemy import select

from connect import SessionLocal
from models import Note, Record, Tag, note_m2m_tag


if __name__ == "__main__":
    with SessionLocal() as session:
        result = (
            session.execute(
                select(
                    Note.id,
                    Note.name,
                    Record.description,
                    Record.done,
                    Tag.name.label("tag"),
                )
                .join(Record, Record.note_id == Note.id)
                .join(note_m2m_tag, note_m2m_tag.c.note_id == Note.id)
                .join(Tag, Tag.id == note_m2m_tag.c.tag_id)
                .where(Tag.name == "food")
            )
            .mappings()
            .all()
        )

        print(result)
