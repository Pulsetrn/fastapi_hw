from pydantic import BaseModel

import uuid

from fastapi_users import schemas

from api.db_models.models import StatusEnum


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


# class UserUpdate(schemas.BaseUserUpdate):
#     pass


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    status: StatusEnum = StatusEnum.PENDING
    priority: int


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: StatusEnum | None = None
    priority: int | None = None


class TodoResponse(TodoCreate):
    id: int
    user_id: uuid.UUID

    class Config:
        orm_mode = True
