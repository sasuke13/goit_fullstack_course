from sqlalchemy import select

from src.db.models import Tag
from sqlalchemy.ext.asyncio import AsyncSession


class TagsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Tag]:
        stmt = select(Tag)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, tag_id: int) -> Tag:
        stmt = select(Tag).filter_by(id=tag_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create(self, tag: Tag) -> Tag:
        self.session.add(Tag(name=tag.name))
        self.session.commit()
        self.session.refresh(tag)
        return tag
