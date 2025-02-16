from pydantic import BaseModel

from lb4.schemas.common import PaginationQuery


class OrderResponse(BaseModel):
    id: int
    name: str


class OrderCreateRequest(BaseModel):
    product_ids: list[int]
