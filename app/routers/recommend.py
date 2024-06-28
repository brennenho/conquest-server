from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.reccomendation.reccomendation import Reccomendations
router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.post("/schedule")
def recommend_courses(courses: list = Body(..., embed=True)):
    ...
