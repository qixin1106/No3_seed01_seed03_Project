from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from tortoise.exceptions import DoesNotExist
import traceback

from models.todo import Todo
from models.user import User
from routes.auth import require_login
from utils.logging import log_exception, log_info, log_warning

# 路由配置
router = APIRouter(tags=["待办事项"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(require_login)):
    """主页 - 显示用户的待办事项"""
    # 获取未完成和已完成的待办事项
    todos = await Todo.filter(user=user).order_by("-create_time").all()
    
    # 分离未完成和已完成的待办
    incomplete_todos = [todo for todo in todos if not todo.is_completed]
    completed_todos = [todo for todo in todos if todo.is_completed]
    
    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "user": user,
            "incomplete_todos": incomplete_todos,
            "completed_todos": completed_todos
        }
    )

@router.post("/add")
async def add_todo(
    request: Request,
    title: str = Form(...),
    content: str = Form(None),
    user: User = Depends(require_login)
):
    """添加新的待办事项"""
    if not title.strip():
        log_warning(f"用户添加待办事项失败：标题不能为空 - 用户：{user.username}")
        return RedirectResponse(url="/?error=标题不能为空", status_code=status.HTTP_303_SEE_OTHER)
    
    try:
        todo = Todo(
            title=title.strip(),
            content=content.strip() if content else None,
            user=user
        )
        await todo.save()
        log_info(f"用户添加待办事项成功：{todo.title} - 用户：{user.username}")
        return RedirectResponse(url="/?message=待办事项添加成功", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        error_msg = f"添加失败：{str(e)}"
        log_exception(e, f"用户添加待办事项失败 - 用户：{user.username}，标题：{title}")
        return RedirectResponse(url=f"/?error={error_msg}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/edit/{todo_id}")
async def edit_todo(
    request: Request,
    todo_id: int,
    title: str = Form(...),
    content: str = Form(None),
    user: User = Depends(require_login)
):
    """编辑待办事项"""
    if not title.strip():
        log_warning(f"用户编辑待办事项失败：标题不能为空 - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url="/?error=标题不能为空", status_code=status.HTTP_303_SEE_OTHER)
    
    try:
        # 确保待办事项属于当前用户
        todo = await Todo.get(id=todo_id, user=user)
        todo.title = title.strip()
        todo.content = content.strip() if content else None
        await todo.save()
        log_info(f"用户编辑待办事项成功：{todo.title} - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url="/?message=待办事项更新成功", status_code=status.HTTP_303_SEE_OTHER)
    except DoesNotExist:
        log_warning(f"用户编辑待办事项失败：待办事项不存在 - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url="/?error=待办事项不存在", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        error_msg = f"更新失败：{str(e)}"
        log_exception(e, f"用户编辑待办事项失败 - 用户：{user.username}，待办ID：{todo_id}，标题：{title}")
        return RedirectResponse(url=f"/?error={error_msg}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/toggle/{todo_id}")
async def toggle_todo(
    request: Request,
    todo_id: int,
    user: User = Depends(require_login)
):
    """标记待办事项为完成/未完成"""
    try:
        todo = await Todo.get(id=todo_id, user=user)
        todo.is_completed = not todo.is_completed
        await todo.save()
        status_str = "已完成" if todo.is_completed else "未完成"
        log_info(f"用户标记待办事项状态：{todo.title} - {status_str} - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except DoesNotExist:
        log_warning(f"用户标记待办事项状态失败：待办事项不存在 - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url="/?error=待办事项不存在", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        error_msg = f"操作失败：{str(e)}"
        log_exception(e, f"用户标记待办事项状态失败 - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url=f"/?error={error_msg}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/delete/{todo_id}")
async def delete_todo(
    request: Request,
    todo_id: int,
    user: User = Depends(require_login)
):
    """删除待办事项"""
    try:
        todo = await Todo.get(id=todo_id, user=user)
        await todo.delete()
        log_info(f"用户删除待办事项成功：{todo.title} - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url="/?message=待办事项删除成功", status_code=status.HTTP_303_SEE_OTHER)
    except DoesNotExist:
        log_warning(f"用户删除待办事项失败：待办事项不存在 - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url="/?error=待办事项不存在", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        error_msg = f"删除失败：{str(e)}"
        log_exception(e, f"用户删除待办事项失败 - 用户：{user.username}，待办ID：{todo_id}")
        return RedirectResponse(url=f"/?error={error_msg}", status_code=status.HTTP_303_SEE_OTHER)