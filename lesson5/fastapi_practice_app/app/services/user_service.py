from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    """Business logic for user use-cases."""

    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def create_user(self, payload: UserCreate):
        """Create a user and enforce email uniqueness."""
        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        return await self.user_repo.create(payload)

    async def get_user(self, user_id: int):
        """Get one user by id or raise 404."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def list_users(self):
        """Return all users."""
        return await self.user_repo.list_all()
