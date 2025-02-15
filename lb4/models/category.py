from tortoise import Model, fields


class Category(Model):
    id: int = fields.BigIntField(pk=True)
    name: str = fields.CharField(max_length=128, index=True)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }