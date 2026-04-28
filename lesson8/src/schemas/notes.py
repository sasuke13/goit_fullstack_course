from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.pagination import Page
from src.schemas.tags import TagResponse


class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)


class NoteModel(NoteBase):
    tags: list[int]


class NoteUpdate(NoteModel):
    done: bool


class NoteStatusUpdate(BaseModel):
    done: bool


class NotePatch(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None
    tags: list[int] | None = None


class NoteResponse(NoteBase):
    id: int
    done: bool
    created_at: datetime | None
    updated_at: datetime | None
    tags: list[TagResponse] | None

    model_config = ConfigDict(from_attributes=True)


class NotePage(Page[NoteResponse]):
    pass
