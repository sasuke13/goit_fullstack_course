from fastapi import APIRouter, Depends, Response
from src.schemas.pagination import PaginationParams
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.notes import NotesService
from src.schemas.notes import NoteModel, NotePage, NoteResponse, NoteUpdate, NotePatch

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=NotePage)
async def get_notes(
    pagination: PaginationParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
    notes_service = NotesService(session)

    return await notes_service.get_all(pagination)


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note_by_id(note_id: int, session: AsyncSession = Depends(get_session)):
    notes_service = NotesService(session)
    note = await notes_service.get_by_id(note_id)

    return note


@router.post("/", response_model=NoteResponse, status_code=201)
async def create_note(note: NoteModel, session: AsyncSession = Depends(get_session)):
    notes_service = NotesService(session)
    note = await notes_service.create(note)
    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int, payload: NoteUpdate, session: AsyncSession = Depends(get_session)
):
    notes_service = NotesService(session)
    note = await notes_service.update(note_id, payload)
    return note


@router.patch("/{note_id}", response_model=NoteResponse)
async def patch_note(note_id: int, payload: NotePatch, session: AsyncSession = Depends(get_session)):
    notes_service = NotesService(session)
    note = await notes_service.patch(note_id, payload)
    return note


@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: int, session: AsyncSession = Depends(get_session)):
    notes_service = NotesService(session)
    await notes_service.delete(note_id)

    return Response(status_code=204)
