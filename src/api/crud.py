from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import asc, desc
from api.db_models.models import Todo
from .pydantic_models.models import TodoCreate, TodoUpdate


async def create_todo(todo_data: TodoCreate, user_id: UUID, session: AsyncSession):
    new_todo = Todo(**todo_data.model_dump(), user_id=user_id)
    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)
    return new_todo


async def get_user_todos(user_id: UUID, session: AsyncSession):
    query = select(Todo).where(Todo.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_todo(todo_id: int, user_id: UUID, session: AsyncSession):
    query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def update_todo(
    todo_id: int, todo_data: TodoUpdate, user_id: UUID, session: AsyncSession
):
    todo = await get_todo(todo_id, user_id, session)
    if todo:
        for key, value in todo_data.model_dump(exclude_unset=True).items():
            setattr(todo, key, value)
        await session.commit()
        await session.refresh(todo)
    return todo


async def delete_todo(todo_id: int, user_id: UUID, session: AsyncSession):
    todo = await get_todo(todo_id, user_id, session)
    if todo:
        await session.delete(todo)
        await session.commit()
    return todo


async def get_top_n_todos(top_n: int, user_id: UUID, session: AsyncSession):
    result = await session.execute(
        select(Todo)
        .where(Todo.user_id == user_id)
        .order_by(desc(Todo.priority))
        .limit(top_n)
    )
    return result.scalars().all()


async def sort_by_criteria(order_by, user_id: UUID, session: AsyncSession):
    result = await session.execute(
        select(Todo).where(Todo.user_id == user_id).order_by(order_by)
    )
    return result.scalars().all()
