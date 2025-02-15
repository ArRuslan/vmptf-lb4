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
