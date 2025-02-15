from __future__ import annotations

from datetime import datetime

from tortoise import fields, Model

from lb4 import models


class Order(Model):
    id: int = fields.BigIntField(pk=True)
    user: models.User = fields.ForeignKeyField("models.User")
    products: fields.ManyToManyRelation[models.Product] = fields.ManyToManyField("models.Product")
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
