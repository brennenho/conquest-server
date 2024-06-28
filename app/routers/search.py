from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.database.postgres_client import PostgresClient

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/search-professor")
def search_professor(
    first_name: str = Body(...), last_name: str = Body(...), department: str = Body(...)
):
    client = PostgresClient()
    # Search with department
    result = client.search_professor_department(
        first_name=first_name, last_name=last_name, department=department
    )
    # If the course title does not match department, example (GESM is not a department) then search by name
    if result == None:
        result = client.search_professor_name(
            first_name=first_name, last_name=last_name
        )
    if result == None:
        return JSONResponse(content={"valid": False}, status_code=401)
    return JSONResponse(content={"valid": True, "result": result}, status_code=200)


@router.post("/search-course")
def search_course(course: str = Body(..., embed=True)):
    client = PostgresClient()
    result = client.search_course(course)
    if len(result) == 0:
        return [None]
    return result
