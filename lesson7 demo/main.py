from pathlib import Path
import time

import aiofiles
from fastapi import Depends, FastAPI, File, Header, HTTPException, Path as FPath, Query, Request, UploadFile, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field, HttpUrl, model_validator
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from db import Note, get_db, init_db

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Lesson 7 FastAPI Demo", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")


class NoteCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=3, max_length=400)
    done: bool = False


class NoteResponse(BaseModel):
    id: int = Field(ge=1)
    name: str
    description: str
    done: bool

    model_config = {"from_attributes": True}


class UserPayload(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    website: HttpUrl
    age: int | None = Field(default=None, ge=13, le=90)
    friends: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def check_friends_logic(self) -> "UserPayload":
        if self.age is not None and self.age < 18 and self.friends > 1000:
            raise ValueError("Too many friends for this age group")
        return self


class ErrorResponse(BaseModel):
    message: str


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = (await db.execute(text("SELECT 1"))).fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


@app.get("/notes/new")
async def read_new_notes():
    return {"message": "Return new notes"}


@app.get("/notes", response_model=list[NoteResponse])
async def read_notes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    q: str | None = Query(default=None, min_length=1, max_length=50),
    db: AsyncSession = Depends(get_db),
):
    query = select(Note)
    if q:
        query = query.where(Note.name.ilike(f"%{q}%"))
    notes = (await db.execute(query.offset(skip).limit(limit))).scalars().all()
    return notes


@app.get("/notes/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: int = FPath(description="The ID of the note to get", gt=0),
    db: AsyncSession = Depends(get_db),
):
    note = (await db.execute(select(Note).where(Note.id == note_id))).scalars().first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    new_note = Note(name=note.name, description=note.description, done=note.done)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note


@app.get("/headers")
async def read_headers(user_agent: str | None = Header(default=None)):
    return {"user_agent": user_agent}


@app.get("/all-headers")
async def read_all_headers(request: Request):
    return {"headers": dict(request.headers)}


@app.post("/users/validate", responses={400: {"model": ErrorResponse}})
async def validate_user(payload: UserPayload):
    if payload.name.lower() == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name admin is reserved")
    return {"message": "User payload is valid"}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    await file.seek(0)
    await _save_uploaded_file(file, file_path)
    return {"file_path": f"/uploads/{file.filename}"}


@app.post("/upload-from-form")
async def upload_from_form(request: Request, file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    await file.seek(0)
    await _save_uploaded_file(file, file_path)
    return {"file_path": str(request.url_for("uploads", path=file.filename))}


async def _save_uploaded_file(file: UploadFile, file_path: Path) -> None:
    async with aiofiles.open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            await buffer.write(chunk)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
