from pydantic import BaseModel

from lb4.schemas.categories import CategoryResponse
from lb4.schemas.common import PaginationQuery


class ProductResponse(BaseModel):
    id: int
    name: str
    category: CategoryResponse
    price: float
    manufacturer: str
    description: str
    created_at: int


class ProductCreateRequest(BaseModel):
    name: str
    category_id: int
    price: float
    manufacturer: str
    description: str


class SearchProductsQuery(PaginationQuery):
    name: str | None = None
    category_id: int | None = None
    price_min: float | None = None
    price_max: float | None = None
