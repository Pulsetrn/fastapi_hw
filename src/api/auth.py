import uuid
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_helper import db_helper
from api.db_models.models import User

SECRET = "SECRET_KEY"


async def get_user_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield SQLAlchemyUserDatabase(session, User)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=JWTStrategy(secret=SECRET, lifetime_seconds=3600),
    get_strategy=get_jwt_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    user_db_model = User


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
