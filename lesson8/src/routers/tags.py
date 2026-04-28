from fastapi import APIRouter, Depends
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.tags import TagsService

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/")
async def get_tags(session: AsyncSession = Depends(get_session)):
    tags_service = TagsService(session)
    return await tags_service.get_all()


@router.get("/{tag_id}")
async def get_tag_by_id(tag_id: int, session: AsyncSession = Depends(get_session)):
    pass


@router.post("/")
async def create_tag(session: AsyncSession = Depends(get_session)):
    pass


@router.put("/{tag_id}")
async def update_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    pass


@router.patch("/{tag_id}")
async def patch_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    pass


@router.delete("/{tag_id}")
async def delete_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    pass
