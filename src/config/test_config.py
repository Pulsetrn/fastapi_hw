from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.db_models.models import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///file:mem_db?mode=memory&cache=shared&uri=true"

test_engine = create_async_engine(
    TEST_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

test_session_factory = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def init_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_test_session():
    async with test_session_factory() as session:
        yield session
