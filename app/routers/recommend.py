from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.recommendation.recommendation import Recommendations

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.post("/schedule")
def recommend_courses(courses: list = Body(..., embed=True)):
    client = Recommendations()
    return client.search_courses(courses)
