from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Note
from src.repository.tags import TagRepository
from src.schemas import NoteModel, NotePage, NoteStatusUpdate, NoteUpdate


class NoteService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tag_repository = TagRepository(db)

    async def create_note(self, body: NoteModel):
        tags = await self.tag_repository.get_tags_by_ids(body.tags)
        payload = body.model_dump(exclude={"tags"}, exclude_unset=True)
        return await Note.create(self.db, payload, tags)

    async def get_notes(self, page: int, per_page: int):
        skip = (page - 1) * per_page
        items = await Note.get_all(self.db, skip, per_page)
        total = await Note.count_all(self.db)
        pages = max(ceil(total / per_page), 1)
        return NotePage(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )

    async def get_note(self, note_id: int):
        return await Note.get_by_id(self.db, note_id)

    async def update_note(self, note_id: int, body: NoteUpdate):
        note = await Note.get_by_id(self.db, note_id)
        if note is None:
            return None
        tags = await self.tag_repository.get_tags_by_ids(body.tags)
        payload = body.model_dump(exclude={"tags"}, exclude_unset=True)
        return await note.update(self.db, payload, tags)

    async def update_status_note(self, note_id: int, body: NoteStatusUpdate):
        note = await Note.get_by_id(self.db, note_id)
        if note is None:
            return None
        return await note.update_status(self.db, body.done)

    async def remove_note(self, note_id: int):
        note = await Note.get_by_id(self.db, note_id)
        if note is None:
            return None
        await note.remove(self.db)
        return note
