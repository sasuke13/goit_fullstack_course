from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from connect import SessionLocal, engine
from models import Base


class ValidatedUser(Base):
    __tablename__ = "validated_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    @validates("username")
    def validate_username(self, key, value: str) -> str:
        if not value or len(value.strip()) < 3:
            raise ValueError("username must contain at least 3 chars")
        return value.strip()

    @validates("age")
    def validate_age(self, key, value: int) -> int:
        if value < 18:
            raise ValueError("user must be 18+")
        return value


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        try:
            user = ValidatedUser(username="Jo", age=17)
            session.add(user)
            session.commit()
        except ValueError as err:
            session.rollback()
            print(f"Validation error: {err}")
