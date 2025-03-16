from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.db_models.models import User
from config.db_helper import db_helper
from pydantic_models.models import TodoCreate, TodoUpdate, TodoResponse
from .crud import (
    create_todo,
    get_user_todos,
    get_todo,
    update_todo,
    delete_todo,
)
from auth import current_active_user

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", response_model=TodoResponse)
async def create(
    todo_data: TodoCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    return await create_todo(todo_data, user.id, session)


@router.get("/", response_model=List[TodoResponse])
async def read_all(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    return await get_user_todos(user.id, session)


@router.get("/{todo_id}", response_model=TodoResponse)
async def read(
    todo_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    todo = await get_todo(todo_id, user.id, session)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update(
    todo_id: int,
    todo_data: TodoUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    updated_todo = await update_todo(todo_id, todo_data, user.id, session)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo


@router.delete("/{todo_id}")
async def delete(
    todo_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    deleted_todo = await delete_todo(todo_id, user.id, session)
    if not deleted_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}
