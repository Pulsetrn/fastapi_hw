import enum
import uuid

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    todos: Mapped[list["Todo"]] = relationship(back_populates="owner")


class StatusEnum(enum.Enum):
    PENDING = "в ожидании"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum), nullable=False, default=StatusEnum.PENDING
    )
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    owner: Mapped["User"] = relationship(back_populates="todos")
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
