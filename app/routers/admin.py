from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_auth_header
from app.scrapers.rmp import RmpParser
from app.api.courses import CourseClient
from app.database.postgres_client import PostgresClient

router = APIRouter(
    prefix="/admin", tags=["admin"], dependencies=[Depends(get_auth_header)]
)


@router.post("/scrape-rmp")
def scrape_rmp():
    try:
        client = PostgresClient()
        parser = RmpParser()
        professors = parser.scrape_all_professors()
        for id, values in professors.items():
            client.add_professor(
                values["first_name"],
                values["last_name"],
                id,
                values["department"],
                values["rating"],
            )
        return JSONResponse(content="success", status_code=200)
    except RuntimeError:
        return JSONResponse(content=False, status_code=500)


@router.post("/scrape-courses")
def scrape_courses():
    client = CourseClient()
    return (client.get_all_departments())
    return JSONResponse(content="succses", status_code=200)
