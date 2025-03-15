from datetime import datetime
from pydantic import BaseModel


class Todo(BaseModel):
    description: str
    status: str
    time_created: datetime
    priority: int
