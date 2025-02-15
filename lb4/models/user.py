from tortoise import Model, fields


class User(Model):
    id: int = fields.BigIntField(pk=True)
    email: str = fields.CharField(max_length=255, unique=True)
    password: str = fields.CharField(max_length=128)
    first_name: str = fields.CharField(max_length=64)
    last_name: str = fields.CharField(max_length=64)
