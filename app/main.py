import asyncio

from fastapi import FastAPI, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import users, watchlist
from app.alerts.scheduler import continuous_check
from app.utils.logger import get_logger
from app.dependencies import get_auth_header
from app.utils.constants import ALLOWED_ORIGINS

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(continuous_check())
    yield
    task.cancel()
    await task


app = FastAPI(lifespan=lifespan)
# app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(watchlist.router)


from app.api.courses import CourseClient
from app.scrapers.courses import CourseParser


@app.get("/")
async def root():
    CourseClient().get_department("csci")
    CourseParser().scrape_deparment("csci")
    # return {"message": message}
