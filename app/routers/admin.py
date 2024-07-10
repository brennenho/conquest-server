from fastapi import APIRouter, Depends
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
    try:
        parser = CourseClient()
        client = PostgresClient()
        response = parser.get_all_departments()
        for department in response:
            for courses in department:
                for course in courses:
                    first_names = []
                    last_names = []
                    for instructor in course["instructor"]:
                        first_names.append(instructor["first_name"])
                        last_names.append(instructor["last_name"])
                    client.add_to_courses(
                        course["section_id"],
                        course["class_name"],
                        first_names,
                        last_names,
                        course["start_time"],
                        course["end_time"],
                        course["days"],
                        course["class_type"],
                    )
        return JSONResponse(content="succses", status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content=False, status_code=500)
