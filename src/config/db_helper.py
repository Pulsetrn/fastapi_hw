from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import DATABASE_URL


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = True,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session

    async def dispose(self):
        await self.engine.dispose()


db_helper = DatabaseHelper(
    url=str(DATABASE_URL),
)
