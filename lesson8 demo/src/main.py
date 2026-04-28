from fastapi import FastAPI

from src.api import notes, tags, utils
from src.settings import settings

app = FastAPI(title="Notes API", version="1.0.0")

app.include_router(utils.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(notes.router, prefix="/api")


def start() -> None:
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=settings.UVICORN_PORT,
        reload=settings.RELOAD,
    )


if __name__ == "__main__":
    start()
