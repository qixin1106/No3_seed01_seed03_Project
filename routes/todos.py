from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models import Todo, User
from routes.auth import require_login

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/todos")
async def todos_page(request: Request, user: User = Depends(require_login)):
    """待办事项页面"""
    # 获取用户的所有待办事项
    todos = await Todo.filter(user=user).order_by("-create_time").all()
    # 分未完成和已完成
    incomplete_todos = [todo for todo in todos if not todo.is_completed]
    completed_todos = [todo for todo in todos if todo.is_completed]
    return templates.TemplateResponse(
        "todos.html",
        {
            "request": request,
            "user": user,
            "incomplete_todos": incomplete_todos,
            "completed_todos": completed_todos
        }
    )


@router.post("/todos/add")
async def add_todo(
    request: Request,
    title: str = Form(...),
    content: str = Form(None),
    user: User = Depends(require_login)
):
    """添加待办事项"""
    if not title.strip():
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

    # 创建待办事项
    await Todo.create(title=title.strip(), content=content.strip() if content else None, user=user)
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/todos/{todo_id}/complete")
async def complete_todo(
    request: Request,
    todo_id: int,
    user: User = Depends(require_login)
):
    """标记待办事项为完成"""
    # 查找用户的待办事项
    todo = await Todo.get_or_none(id=todo_id, user=user)
    if not todo:
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

    # 标记为完成
    todo.is_completed = True
    await todo.save()
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/todos/{todo_id}/uncomplete")
async def uncomplete_todo(
    request: Request,
    todo_id: int,
    user: User = Depends(require_login)
):
    """标记待办事项为未完成"""
    # 查找用户的待办事项
    todo = await Todo.get_or_none(id=todo_id, user=user)
    if not todo:
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

    # 标记为未完成
    todo.is_completed = False
    await todo.save()
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/todos/{todo_id}/delete")
async def delete_todo(
    request: Request,
    todo_id: int,
    user: User = Depends(require_login)
):
    """删除待办事项"""
    # 查找用户的待办事项
    todo = await Todo.get_or_none(id=todo_id, user=user)
    if not todo:
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

    # 删除待办事项
    await todo.delete()
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/todos/{todo_id}/edit")
async def edit_todo(
    request: Request,
    todo_id: int,
    title: str = Form(...),
    content: str = Form(None),
    user: User = Depends(require_login)
):
    """编辑待办事项"""
    if not title.strip():
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

    # 查找用户的待办事项
    todo = await Todo.get_or_none(id=todo_id, user=user)
    if not todo:
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

    # 更新待办事项
    todo.title = title.strip()
    todo.content = content.strip() if content else None
    await todo.save()
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)