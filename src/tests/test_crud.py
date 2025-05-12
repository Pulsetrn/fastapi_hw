from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import (
    create_todo,
    delete_todo,
    get_todo,
    get_top_n_todos,
    get_user_todos,
    sort_by_criteria,
    update_todo,
)
from api.db_models.models import StatusEnum, Todo
from api.pydantic_models.models import TodoCreate, TodoResponse, TodoUpdate
from config.test_config import test_session_factory

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def db_session():
    async with test_session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def test_user_id():
    return uuid4()


@pytest_asyncio.fixture
async def test_todo(db_session, test_user_id):
    todo_data = TodoCreate(
        title="Test Todo", description="Test Description", priority=1
    )
    todo = await create_todo(todo_data, test_user_id, db_session)
    return todo


async def test_create_todo(db_session, test_user_id):
    todo_data = TodoCreate(title="New Todo", description="New Description", priority=2)

    todo = await create_todo(todo_data, test_user_id, db_session)

    assert todo.title == "New Todo"
    assert todo.description == "New Description"
    assert todo.priority == 2
    assert todo.user_id == test_user_id
    assert todo.status == StatusEnum.PENDING


async def test_get_todo(db_session, test_todo, test_user_id):
    retrieved_todo = await get_todo(test_todo.id, test_user_id, db_session)

    assert retrieved_todo is not None
    assert retrieved_todo.id == test_todo.id
    assert retrieved_todo.title == test_todo.title


async def test_get_user_todos(db_session, test_user_id, test_todo):
    todos = await get_user_todos(test_user_id, db_session)

    assert len(todos) == 1
    assert todos[0].id == test_todo.id
    assert todos[0].user_id == test_user_id


async def test_update_todo(db_session, test_todo, test_user_id):
    update_data = TodoUpdate(
        title="Updated Todo",
        description="Updated Description",
        status=StatusEnum.IN_PROGRESS,
        priority=3,
    )

    updated_todo = await update_todo(
        test_todo.id, update_data, test_user_id, db_session
    )

    assert updated_todo.title == "Updated Todo"
    assert updated_todo.description == "Updated Description"
    assert updated_todo.status == StatusEnum.IN_PROGRESS
    assert updated_todo.priority == 3


async def test_delete_todo(db_session, test_todo, test_user_id):
    await delete_todo(test_todo.id, test_user_id, db_session)

    deleted_todo = await get_todo(test_todo.id, test_user_id, db_session)
    assert deleted_todo is None


async def test_sort_todos(db_session, test_user_id):
    todos_data = [
        TodoCreate(title=f"Todo {i}", description=f"Description {i}", priority=i)
        for i in range(3)
    ]

    for todo_data in todos_data:
        await create_todo(todo_data, test_user_id, db_session)

    sorted_todos = await sort_by_criteria("priority", test_user_id, db_session)
    assert len(sorted_todos) == 3
    assert sorted_todos[0].priority == 0
    assert sorted_todos[-1].priority == 2


async def test_get_top_n_todos(db_session, test_user_id):
    todos_data = [
        TodoCreate(title=f"Todo {i}", description=f"Description {i}", priority=i)
        for i in range(5)
    ]

    for todo_data in todos_data:
        await create_todo(todo_data, test_user_id, db_session)

    top_todos = await get_top_n_todos(3, test_user_id, db_session)
    assert len(top_todos) == 3
    assert all(todo.priority >= 2 for todo in top_todos)
    assert len(top_todos) == 3
    assert all(todo.priority >= 2 for todo in top_todos)
