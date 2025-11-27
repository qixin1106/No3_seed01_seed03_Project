from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.sessions import SessionMiddleware
from routes.auth import router as auth_router
from routes.todos import router as todos_router
import os
import logging
from datetime import datetime

app = FastAPI()

# 配置日志记录
log_file = f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器，记录异常日志"""
    logger.error(f"Exception occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )

# 配置静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置模板
templates = Jinja2Templates(directory="templates")

# 配置Session中间件
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24).hex())

# 注册路由
app.include_router(auth_router, prefix="", tags=["auth"])
app.include_router(todos_router, prefix="", tags=["todos"])

# 配置Tortoise-ORM
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root(request: Request):
    """根路径重定向到登录页"""
    return templates.TemplateResponse("login.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
