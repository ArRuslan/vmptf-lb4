from __future__ import annotations

from datetime import datetime

from tortoise import fields, Model

from lb4 import models


class Order(Model):
    id: int = fields.BigIntField(pk=True)
    user: models.User = fields.ForeignKeyField("models.User")
    products: fields.ManyToManyRelation[models.Product] = fields.ManyToManyField("models.Product")
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    async def to_json(self, prefetched_products: list[models.Product] | None = None) -> dict:
        products = prefetched_products if prefetched_products is not None else await self.products.all()\
            .select_related("category")

        return {
            "id": self.id,
            "products": [product.to_json() for product in products],
            "created_at": int(self.created_at.timestamp()),
        }
