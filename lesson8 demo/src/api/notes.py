from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.pagination import PaginationParams
from src.db.session import get_db
from src.schemas import NoteModel, NotePage, NoteResponse, NoteStatusUpdate, NoteUpdate
from src.services.notes import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=NotePage)
async def read_notes(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    note_service = NoteService(db)
    return await note_service.get_notes(pagination.page, pagination.per_page)


@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note_service = NoteService(db)
    note = await note_service.get_note(note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(body: NoteModel, db: AsyncSession = Depends(get_db)):
    note_service = NoteService(db)
    return await note_service.create_note(body)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    body: NoteUpdate, note_id: int, db: AsyncSession = Depends(get_db)
):
    note_service = NoteService(db)
    note = await note_service.update_note(note_id, body)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_status_note(
    body: NoteStatusUpdate, note_id: int, db: AsyncSession = Depends(get_db)
):
    note_service = NoteService(db)
    note = await note_service.update_status_note(note_id, body)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.delete("/{note_id}", response_model=NoteResponse)
async def remove_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note_service = NoteService(db)
    note = await note_service.remove_note(note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note
