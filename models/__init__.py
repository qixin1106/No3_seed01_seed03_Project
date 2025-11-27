from tortoise.models import Model
from tortoise import fields
from datetime import datetime


class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=20, unique=True, index=True)
    password_hash = fields.CharField(max_length=128)
    create_time = fields.DatetimeField(default=datetime.now)

    class Meta:
        table = "users"
        ordering = ["-create_time"]


class Todo(Model):
    id = fields.IntField(pk=True, index=True)
    title = fields.CharField(max_length=100, null=False)
    content = fields.TextField(null=True)
    is_completed = fields.BooleanField(default=False)
    create_time = fields.DatetimeField(default=datetime.now)
    user = fields.ForeignKeyField("models.User", related_name="todos")

    class Meta:
        table = "todos"
        ordering = ["-create_time"]