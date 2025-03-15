from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    todos: Mapped[list["Todo"]] = relationship(back_populates="owner")


class StatusEnum(enum.Enum):
    PENDING = "в ожидании"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class Todo(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum), nullable=False, default=StatusEnum.PENDING
    )
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    owner: Mapped["User"] = relationship(back_populates="todos")
