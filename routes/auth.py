from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt
from tortoise.exceptions import IntegrityError
from models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def get_current_user(request: Request):
    """获取当前登录用户"""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return await User.get_or_none(id=user_id)


async def require_login(request: Request):
    """要求用户登录的依赖项"""
    user = await get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    return user


@router.get("/register")
async def register_page(request: Request):
    """注册页面"""
    user = await get_current_user(request)
    if user:
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    """处理注册请求"""
    # 验证输入
    if len(username) < 3 or len(username) > 20:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "用户名长度必须在3-20位之间"}
        )
    if len(password) < 6 or len(password) > 16:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "密码长度必须在6-16位之间"}
        )
    if password != confirm_password:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "两次输入的密码不一致"}
        )

    # 加密密码
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        # 创建用户
        user = await User.create(username=username, password_hash=password_hash)
        # 注册成功后跳转到登录页
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    except IntegrityError:
        # 用户名已存在
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "用户名已存在"}
        )


@router.get("/login")
async def login_page(request: Request):
    """登录页面"""
    user = await get_current_user(request)
    if user:
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """处理登录请求"""
    # 查找用户
    user = await User.get_or_none(username=username)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "用户名或密码错误"}
        )

    # 验证密码
    if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "用户名或密码错误"}
        )

    # 登录成功，设置session
    request.session["user_id"] = user.id
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout")
async def logout(request: Request):
    """处理退出请求"""
    # 清除session
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)