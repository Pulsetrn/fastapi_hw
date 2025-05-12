import uuid

from fastapi import Depends
from fastapi_users import FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.manager import BaseUserManager
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from api.db_models.models import User
from config.db_helper import db_helper

SECRET = "SECRET_KEY"


async def get_user_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield SQLAlchemyUserDatabase(session, User)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
