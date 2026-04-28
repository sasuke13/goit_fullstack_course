from models.base import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = "users"

    username = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(10), nullable=False)
