from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("TEST_CONFIG__DB__URL")
