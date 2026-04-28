from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    """Data access layer for user entities."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: UserCreate) -> User:
        """Persist a new user and return the saved entity."""
        user = User(email=payload.email, full_name=payload.full_name, age=payload.age)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        """Fetch a user by primary key."""
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by unique email."""
        stmt = select(User).where(User.email == email)
        return await self.session.scalar(stmt)

    async def list_all(self) -> list[User]:
        """Return all users ordered by id."""
        stmt = select(User).order_by(User.id)
        result = await self.session.scalars(stmt)
        return list(result.all())
