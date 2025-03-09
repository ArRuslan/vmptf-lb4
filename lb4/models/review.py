from __future__ import annotations

from datetime import datetime

from tortoise import fields, Model

from lb4 import models


class Review(Model):
    id: int = fields.BigIntField(pk=True)
    user: models.User = fields.ForeignKeyField("models.User")
    product: models.Product = fields.ForeignKeyField("models.Product")
    rating: float = fields.FloatField()
    text: str | None = fields.TextField(null=True, default=None)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    product_id: int

    async def to_json(self) -> dict:
        self.user = await self.user

        return {
            "id": self.id,
            "user": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            },
            "product_id": self.product_id,
            "rating": self.rating,
            "text": self.text,
            "created_at": self.created_at,
        }
