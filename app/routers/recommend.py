from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.recommendation.recommendation import Recommendations, CourseSearcher

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.post("/schedule")
def recommend_courses(courses: list = Body(..., embed=True)):
    client = CourseSearcher()
    return client.get_recommendations(courses)
