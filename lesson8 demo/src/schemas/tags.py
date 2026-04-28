from pydantic import BaseModel, ConfigDict, Field

from src.schemas.pagination import Page

class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TagPage(Page[TagResponse]):
    pass
