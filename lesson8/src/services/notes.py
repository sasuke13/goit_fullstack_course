from math import ceil

from fastapi import HTTPException

from src.db.models import Note
from src.repositories.notes import NotesRepository
from src.repositories.tags import TagsRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.notes import NoteModel, NotePage, NotePatch, NoteUpdate
from src.schemas.pagination import PaginationParams


class NotesService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.notes_repository = NotesRepository(session)
        self.tags_repository = TagsRepository(session)

    async def get_all(self, pagination: PaginationParams) -> NotePage:
        skip = (pagination.page - 1) * pagination.per_page
        notes = await self.notes_repository.get_all(skip, pagination.per_page)

        total = await self.notes_repository.count_all()
        pages = max(ceil(total / pagination.per_page), 1)

        return NotePage(
            items=notes,
            total=total,
            page=pagination.page,
            per_page=pagination.per_page,
            pages=pages,
            has_next=pagination.page < pages,
            has_prev=pagination.page > 1,
        )

    async def get_by_id(self, note_id: int) -> Note:
        note = await Note.get_by_id(self.session, note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        return note

    async def create(self, note: NoteModel) -> Note:
        tags = []
        for tag in note.tags:
            tag = await self.tags_repository.get_by_id(tag)
            if tag is None:
                raise HTTPException(status_code=404, detail="Tag not found")
            tags.append(tag)

        note = await self.notes_repository.create(
            note.model_dump(exclude={"tags"}), tags
        )
        return note

    async def update(self, note_id: int, payload: NoteUpdate) -> Note:
        note = await self.get_by_id(note_id)

        tags = []
        for tag in payload.tags:
            tag = await self.tags_repository.get_by_id(tag)
            if tag is None:
                raise HTTPException(status_code=404, detail="Tag not found")
            tags.append(tag)

        note = await self.notes_repository.update(
            note, payload.model_dump(exclude={"tags"}), tags
        )
        return note

    async def patch(self, note_id: int, payload: NotePatch) -> Note:
        note = await self.get_by_id(note_id)

        tags = None
        if payload.tags is not None:
            tags = []
            for tag in payload.tags:
                tag = await self.tags_repository.get_by_id(tag)
                if tag is None:
                    raise HTTPException(status_code=404, detail="Tag not found")
                tags.append(tag)

        note = await self.notes_repository.update(
            note, payload.model_dump(exclude_none=True, exclude={"tags"}), tags
        )
        return note

    async def delete(self, note_id: int) -> None:
        note = await self.get_by_id(note_id)

        await self.notes_repository.delete(note)
