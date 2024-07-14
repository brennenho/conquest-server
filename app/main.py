import asyncio
import os

from fastapi import FastAPI, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import search, users, watchlist, admin
from app.alerts.scheduler import continuous_check
from app.utils.logger import get_logger

logger = get_logger(__name__)


# Check watchlist at a set interval while server is running
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(continuous_check())
    yield
    task.cancel()
    await task


root_path = ""
if os.environ.get("TARGET") == "production":
    root_path = "/conquest-api"

app = FastAPI(lifespan=lifespan, root_path=root_path)

# Validate API requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(watchlist.router)
app.include_router(search.router)


# Root endpoint for health checks
@app.get("/")
async def root():
    return {"status": "ok"}
