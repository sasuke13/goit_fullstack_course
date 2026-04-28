from fastapi import FastAPI
from src.settings import settings
from src.routers.notes import router as notes_router
from src.routers.tags import router as tags_router

app = FastAPI(title="Notes App", version="0.1.0")

app.include_router(notes_router)
app.include_router(tags_router)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.UVICORN_PORT,
        reload=settings.RELOAD,
    )


if __name__ == "__main__":
    main()
