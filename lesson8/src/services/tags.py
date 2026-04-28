from fastapi import HTTPException

from src.db.models import Tag
from src.repositories.tags import TagsRepository
from sqlalchemy.ext.asyncio import AsyncSession


class TagsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.tags_repository = TagsRepository(session)

    async def get_all(self) -> list[Tag]:
        tags = await self.tags_repository.get_all()
        return tags

    async def get_by_id(self, tag_id: int) -> Tag:
        tag = await self.tags_repository.get_by_id(tag_id)
        if tag is None:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag
