import asyncio

from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from app.routers import users
from app.alerts.scheduler import continuous_check
from app.utils.logger import get_logger
from app.dependencies import get_auth_header

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(continuous_check())
    yield
    task.cancel()
    await task


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)


@app.get("/")
async def root(token=Depends(get_auth_header)):
    return {"message": "Hello World"}
