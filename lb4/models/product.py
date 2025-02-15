from __future__ import annotations

from datetime import datetime

from tortoise import fields, Model

from lb4 import models


class Product(Model):
    id: int = fields.BigIntField(pk=True)
    name: str = fields.CharField(max_length=255, index=True)
    manufacturer: str = fields.CharField(max_length=255)
    description: str = fields.TextField(default="")
    price: float = fields.FloatField()
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    category: models.Category = fields.ForeignKeyField("models.Category")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "description": self.description,
            "price": self.price,
            "created_at": int(self.created_at.timestamp()),
            "category": self.category.to_json(),
        }
