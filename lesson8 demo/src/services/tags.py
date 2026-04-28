from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.tags import TagRepository
from src.schemas import TagModel, TagPage


class TagService:
    def __init__(self, db: AsyncSession):
        self.repository = TagRepository(db)

    async def create_tag(self, body: TagModel):
        return await self.repository.create_tag(body)

    async def get_tags(self, page: int, per_page: int):
        skip = (page - 1) * per_page
        items = await self.repository.get_tags(skip, per_page)
        total = await self.repository.count_tags()
        pages = max(ceil(total / per_page), 1)
        return TagPage(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )

    async def get_tag(self, tag_id: int):
        return await self.repository.get_tag_by_id(tag_id)

    async def update_tag(self, tag_id: int, body: TagModel):
        return await self.repository.update_tag(tag_id, body)

    async def remove_tag(self, tag_id: int):
        return await self.repository.remove_tag(tag_id)
