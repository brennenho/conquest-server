from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.recommendation.recommendation import CourseSearcher

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.post("/schedule")
def recommend_courses(courses: list = Body(..., embed=True)):
    client = CourseSearcher()
    result = client.get_recommendations(courses)
    if len(result) == 0:
        return JSONResponse(content={"isValid": False}, status_code=406)
    return JSONResponse(content=result, status_code=200)
