import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.alerts.scheduler import continuous_check
from app.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(continuous_check())
    yield
    task.cancel()
    await task


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}
