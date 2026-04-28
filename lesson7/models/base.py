from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
