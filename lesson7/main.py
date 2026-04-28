from pathlib import Path

import time
import aiofiles
from fastapi import FastAPI, Depends, HTTPException, status, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from schemas.user_schemas import UserRequestSchema
from schemas.default_schemas import ErrorResponseSchema
from db import init_db, get_db
from models.user import User

app = FastAPI(title="My API", description="This is a simple API", version="0.1.0")
BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    await init_db()


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc), "path": request.url.path})


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/users/{user_id}", responses={200: {"model": UserRequestSchema}, 404: {"model": ErrorResponseSchema}})
async def get_user(
    user_id: int,
    db = Depends(get_db)
):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise Exception("User not found")
    return db_user


@app.post("/users", responses={200: {"model": UserRequestSchema}})
async def create_user(
    user: UserRequestSchema,
    db = Depends(get_db)
):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


@app.post("/upload-from-form")
async def upload_from_form(request: Request, file: UploadFile = File(..., description="The file to upload")):
    file_path = MEDIA_DIR / file.filename
    await file.seek(0)
    
    async with aiofiles.open(file_path, "wb") as buffer:
        while chunk :=await file.read(1024):
            await buffer.write(chunk)
    
    return {"file_path": str(request.url_for("media", path=file.filename))}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
