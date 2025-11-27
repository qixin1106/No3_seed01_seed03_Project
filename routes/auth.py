from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from datetime import datetime, timedelta
from tortoise.exceptions import IntegrityError
import traceback

from models.user import User
from utils.logging import log_exception, log_info, log_warning

# 路由配置
router = APIRouter(prefix="/auth", tags=["认证"])
templates = Jinja2Templates(directory="templates")

# JWT配置
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    """创建JWT令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """验证JWT令牌并返回用户"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    # 异步获取用户，需要在依赖中使用
    return username

async def get_current_user(request: Request):
    """获取当前登录用户"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    username = verify_token(token)
    if not username:
        return None
    
    user = await User.get_or_none(username=username)
    return user

async def require_login(request: Request):
    """登录验证依赖，未登录则重定向到登录页"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Not authenticated",
            headers={"Location": "/auth/login"}
        )
    return user

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """注册页面"""
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    """用户注册"""
    # 验证表单数据
    errors = []
    
    if len(username) < 3 or len(username) > 20:
        errors.append("用户名长度必须在3-20位之间")
    
    if len(password) < 6 or len(password) > 16:
        errors.append("密码长度必须在6-16位之间")
    
    if password != confirm_password:
        errors.append("两次输入的密码不一致")
    
    if errors:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "errors": errors, "username": username}
        )
    
    try:
        # 创建用户
        user = User(
            username=username,
            password_hash=User.get_password_hash(password)
        )
        await user.save()
        
        # 记录注册成功日志
        log_info(f"用户注册成功：{username}")
        
        # 注册成功，重定向到登录页
        return RedirectResponse(url="/auth/login?message=注册成功，请登录", status_code=status.HTTP_303_SEE_OTHER)
        
    except IntegrityError:
        errors.append("用户名已存在")
        log_warning(f"用户注册失败：用户名已存在 - {username}")
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "errors": errors, "username": username}
        )
    except Exception as e:
        error_msg = f"注册失败：{str(e)}"
        errors.append(error_msg)
        
        # 记录异常日志
        log_exception(e, f"用户注册失败 - 用户名：{username}")
        
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "errors": errors, "username": username}
        )

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, message: str = None):
    """登录页面"""
    return templates.TemplateResponse("auth/login.html", {"request": request, "message": message})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """用户登录"""
    errors = []
    
    # 验证用户
    user = await User.get_or_none(username=username)
    if not user or not user.verify_password(password):
        errors.append("用户名或密码错误")
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "errors": errors, "username": username}
        )
    
    # 创建JWT令牌
    access_token = create_access_token(data={"sub": user.username})
    
    # 设置cookie并跳转主页
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return response

@router.post("/logout")
async def logout(request: Request):
    """用户退出"""
    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response