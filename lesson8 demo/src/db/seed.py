import asyncio

from sqlalchemy import select

from src.db.models import Note, Tag
from src.db.session import session_manager


async def seed() -> None:
    async with session_manager.session() as session:
        tag_names = ["work", "study", "personal"]
        tags_map: dict[str, Tag] = {}

        for name in tag_names:
            existing = await session.execute(select(Tag).where(Tag.name == name))
            tag = existing.scalar_one_or_none()
            if tag is None:
                tag = Tag(name=name)
                session.add(tag)
                await session.flush()
            tags_map[name] = tag

        existing_notes = await session.execute(select(Note.id).limit(1))
        if existing_notes.scalar_one_or_none() is None:
            notes_payload = [
                {
                    "title": "Buy groceries",
                    "description": "Milk, bread, and fruits",
                    "done": False,
                    "tags": [tags_map["personal"]],
                },
                {
                    "title": "Prepare lesson",
                    "description": "Create REST API examples for students",
                    "done": False,
                    "tags": [tags_map["study"], tags_map["work"]],
                },
                {
                    "title": "Review pull request",
                    "description": "Check notes and tags endpoints",
                    "done": True,
                    "tags": [tags_map["work"]],
                },
            ]
            for item in notes_payload:
                note = Note(
                    title=item["title"],
                    description=item["description"],
                    done=item["done"],
                    tags=item["tags"],
                )
                session.add(note)

        await session.commit()


def run_seed() -> None:
    asyncio.run(seed())
