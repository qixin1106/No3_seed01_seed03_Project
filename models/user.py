from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext
from datetime import datetime

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Model):
    """用户模型"""
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=20, unique=True, index=True, description="用户名")
    password_hash = fields.CharField(max_length=128, description="密码哈希值")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "users"
        ordering = ["-create_time"]

    def verify_password(self, password: str) -> bool:
        """验证密码是否正确"""
        return pwd_context.verify(password, self.password_hash)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """生成密码哈希值，自动截断超过72字节的密码"""
        # bcrypt算法最多支持72字节的密码
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            # 确保截断后的字节是有效的UTF-8字符串
            password = password_bytes.decode('utf-8', errors='replace')
        # 使用截断后的密码生成哈希值
        return pwd_context.hash(password)

    def __str__(self):
        return self.username