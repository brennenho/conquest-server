import asyncio

from fastapi import FastAPI, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import search, users, watchlist, admin
from app.alerts.scheduler import continuous_check
from app.utils.logger import get_logger
from app.utils.constants import ALLOWED_ORIGINS

logger = get_logger(__name__)


# checks watchlist every interval while server is running
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(continuous_check())
    yield
    task.cancel()
    await task


app = FastAPI(lifespan=lifespan)
# app = FastAPI()

# authentication to validate api requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(users.router)
app.include_router(watchlist.router)
app.include_router(search.router)
