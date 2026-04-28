from contextlib import asynccontextmanager

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.models.task import Task
from app.models.user import User
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize database tables when the app starts."""
    # Import models before create_all so metadata includes all tables.
    _ = (User, Task)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
app.include_router(api_router, prefix=settings.api_v1_prefix)
