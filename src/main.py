import uvicorn
from fastapi import FastAPI
from api.auth import fastapi_users, auth_backend
from api import router as api_router
from api.pydantic_models.models import UserCreate, UserRead

app = FastAPI()
app.include_router(api_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
