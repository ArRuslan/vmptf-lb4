from pydantic import BaseModel

from lb4.schemas.common import PaginationQuery


class CategoryResponse(BaseModel):
    id: int
    name: str


class CategoryCreateRequest(BaseModel):
    name: str


class SearchCategoriesQuery(PaginationQuery):
    name: str | None = None