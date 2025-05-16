import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from config.db_helper import db_helper
from config.test_config import get_test_session, init_test_db, test_session_factory
from main import app

app.dependency_overrides[db_helper.session_getter] = get_test_session

client = TestClient(app)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_test_db():
    await init_test_db()
    yield


@pytest.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def access_token():
    client.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "password": "test",
        },
    )
    response = client.post(
        "/auth/jwt/login",
        data={"username": "test@test.com", "password": "test"},
    )
    return response.json()["access_token"]


@pytest.fixture
def todo_id(access_token):
    response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Test Todo", "description": "Test Description", "priority": 1},
    )
    return response.json()["id"]


def test_create_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "test2@test.com",
            "password": "test",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test2@test.com"


def test_login_user(access_token):
    assert access_token is not None


def test_create_todo(access_token):
    response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Test Todo", "description": "Test Description", "priority": 1},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"


def test_get_todos(access_token, todo_id):
    response = client.get(
        "/todos",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_update_todo(access_token, todo_id):
    response = client.put(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Updated Todo",
            "description": "Updated Description",
            "priority": 2,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Todo"


def test_sort_todos(access_token, todo_id):
    response = client.get(
        "/todos/criteria-sort/",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"sort_by": "title"},
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_top_n_todos(access_token, todo_id):
    response = client.get(
        "/todos/top-priority/",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"top_n": 1},
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_search_todos(access_token, todo_id):
    response = client.get(
        "/todos/search/",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"query": "Test"},
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_delete_todo(access_token, todo_id):
    response = client.delete(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
