from tortoise.models import Model
from tortoise import fields
from datetime import datetime

class Todo(Model):
    """待办事项模型"""
    id = fields.IntField(pk=True, index=True)
    title = fields.CharField(max_length=100, description="待办事项标题")
    content = fields.TextField(null=True, description="待办事项描述")
    is_completed = fields.BooleanField(default=False, description="是否已完成")
    priority = fields.IntField(default=1, description="优先级(1-5)")
    due_date = fields.DatetimeField(null=True, description="截止日期")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    
    # 外键关联用户
    user = fields.ForeignKeyField("models.User", related_name="todos", on_delete=fields.CASCADE)

    class Meta:
        table = "todos"
        ordering = ["-create_time"]

    def __str__(self):
        return self.title