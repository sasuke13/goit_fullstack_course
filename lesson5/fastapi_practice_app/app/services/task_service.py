from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class TaskService:
    """Business logic for task use-cases."""

    def __init__(self, session: AsyncSession):
        self.task_repo = TaskRepository(session)
        self.user_repo = UserRepository(session)

    async def create_task(self, payload: TaskCreate):
        """Create a task only if the owner exists."""
        owner = await self.user_repo.get_by_id(payload.owner_id)
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found"
            )
        return await self.task_repo.create(payload)

    async def list_tasks(self):
        """Return all tasks."""
        return await self.task_repo.list_all()

    async def update_task(self, task_id: int, payload: TaskUpdate):
        """Update a task by id."""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        return await self.task_repo.update(task, payload)

    async def delete_task(self, task_id: int):
        """Delete a task by id."""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        await self.task_repo.delete(task)
