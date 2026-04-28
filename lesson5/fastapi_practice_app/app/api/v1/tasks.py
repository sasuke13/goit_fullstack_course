from app.api.deps import db_session_dep
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate,
    session: AsyncSession = Depends(db_session_dep),
) -> TaskRead:
    """Create a new task for an existing user."""
    service = TaskService(session)
    return await service.create_task(payload)


@router.get("", response_model=list[TaskRead])
async def list_tasks(session: AsyncSession = Depends(db_session_dep)) -> list[TaskRead]:
    """Return all tasks ordered by id."""
    service = TaskService(session)
    return await service.list_tasks()


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    session: AsyncSession = Depends(db_session_dep),
) -> TaskRead:
    """Update task fields by id."""
    service = TaskService(session)
    return await service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int, session: AsyncSession = Depends(db_session_dep)
) -> Response:
    """Delete a task by id."""
    service = TaskService(session)
    await service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
