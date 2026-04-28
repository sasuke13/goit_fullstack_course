from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository:
    """Data access layer for task entities."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: TaskCreate) -> Task:
        """Persist a new task and return the saved entity."""
        task = Task(title=payload.title, owner_id=payload.owner_id)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: int) -> Task | None:
        """Fetch a task by primary key."""
        return await self.session.get(Task, task_id)

    async def list_all(self) -> list[Task]:
        """Return all tasks ordered by id."""
        stmt = select(Task).order_by(Task.id)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def update(self, task: Task, payload: TaskUpdate) -> Task:
        """Apply partial update to a task and persist changes."""
        if payload.title is not None:
            task.title = payload.title
        if payload.is_done is not None:
            task.is_done = payload.is_done

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        """Delete a task and commit transaction."""
        await self.session.delete(task)
        await self.session.commit()
