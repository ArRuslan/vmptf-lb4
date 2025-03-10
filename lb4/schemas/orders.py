from pydantic import BaseModel

from .products import ProductResponse


class OrderResponse(BaseModel):
    id: int
    products: list[ProductResponse]
    created_at: int


class OrderCreateRequest(BaseModel):
    product_ids: list[int]
