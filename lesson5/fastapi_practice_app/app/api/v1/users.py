from app.api.deps import db_session_dep
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(db_session_dep),
) -> UserRead:
    """Create a new user if email is unique."""
    service = UserService(session)
    return await service.create_user(payload)


@router.get("", response_model=list[UserRead])
async def list_users(session: AsyncSession = Depends(db_session_dep)) -> list[UserRead]:
    """Return all users ordered by id."""
    service = UserService(session)
    return await service.list_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int, session: AsyncSession = Depends(db_session_dep)
) -> UserRead:
    """Return one user by id."""
    service = UserService(session)
    return await service.get_user(user_id)
