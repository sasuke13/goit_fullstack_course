from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.db.models import Note, Tag
from sqlalchemy.ext.asyncio import AsyncSession


class NotesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def count_all(self) -> int:
        stmt = select(func.count(Note.id))
        result = await self.session.execute(stmt)

        return int(result.scalar_one())

    async def get_all(self, skip: int, per_page: int) -> list[Note]:
        stmt = (
            select(Note).options(selectinload(Note.tags)).offset(skip).limit(per_page)
        )
        result = await self.session.execute(stmt)

        return result.scalars().all()

    # async def get_by_id(self, note_id: int) -> Note:
    #     stmt = select(Note).options(selectinload(Note.tags)).filter_by(id=note_id)
    #     result = await self.session.execute(stmt)

    #     return result.scalar_one_or_none()

    async def create(self, note: dict, tags: list[Tag]) -> Note:
        db_note = Note(**note, tags=tags)
        self.session.add(db_note)
        await self.session.flush()
        note_id = db_note.id
        await self.session.commit()
        stmt = select(Note).options(selectinload(Note.tags)).filter_by(id=note_id)
        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def update(self, note: Note, payload: dict, tags: list[Tag]) -> Note:
        for key, value in payload.items():
            setattr(note, key, value)
        note.tags = tags if tags is not None else note.tags
        await self.session.commit()
        await self.session.refresh(note)

        updated_note = await self.get_by_id(note.id)
        return updated_note

    async def patch(self, note: Note, payload: dict, tags: list[Tag]) -> Note:
        for key, value in payload.items():
            setattr(note, key, value)
        self.tags = tags
        await self.session.commit()
        await self.session.refresh(note)

        updated_note = await self.get_by_id(note.id)
        return updated_note

    async def delete(self, note: Note) -> None:
        await self.session.delete(note)
        await self.session.commit()
