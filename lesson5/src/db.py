from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (AsyncEngine, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import Session, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

SYNC_DB_URL = f"sqlite+pysqlite:///{DATA_DIR / 'practice.db'}"
ASYNC_DB_URL = f"sqlite+aiosqlite:///{DATA_DIR / 'practice_async.db'}"


def get_engine(echo: bool = True) -> Engine:
    return create_engine(SYNC_DB_URL, echo=echo, future=True)


def get_session_factory(echo: bool = True) -> sessionmaker[Session]:
    engine = get_engine(echo=echo)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_async_engine(echo: bool = True) -> AsyncEngine:
    return create_async_engine(ASYNC_DB_URL, echo=echo, future=True)


def get_async_session_factory(echo: bool = True) -> async_sessionmaker:
    engine = get_async_engine(echo=echo)
    return async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
