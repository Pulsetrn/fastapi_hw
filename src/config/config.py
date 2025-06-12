import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "TEST_CONFIG__DB__URL",
    "postgresql+asyncpg://user:password@pg:5432/todo",
)
