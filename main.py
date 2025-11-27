from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
import uvicorn

from routes import auth, todo

# 创建FastAPI应用
app = FastAPI(
    title="待办系统",
    description="FastAPI + Tortoise-ORM + Jinja2 待办系统",
    version="1.0.0"
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
app.include_router(auth.router)
app.include_router(todo.router)

# Tortoise-ORM配置
register_tortoise(
    app,
    db_url="sqlite://todo.db",  # SQLite数据库
    modules={"models": ["models.user", "models.todo"]},  # 模型模块
    generate_schemas=True,  # 自动生成数据库表
    add_exception_handlers=True,  # 添加异常处理器
)

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

if __name__ == "__main__":
    # 启动FastAPI应用
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,  # 开发模式下启用热重载
        log_level="info"
    )