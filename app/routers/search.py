from fastapi import APIRouter, Body, Response
from fastapi.responses import JSONResponse
from app.database.postgres_client import PostgresClient

# This router handles all search tasks from the extension

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/search-professor")
def search_professor(
    first_name: str = Body(...), last_name: str = Body(...), department: str = Body(...)
):
    """
    Search for a professor based on their first name, last name, and department.

    Args:
        first_name (str): The first name of the professor.
        last_name (str): The last name of the professor.
        department (str): The department of the professor.

    Returns:
        JSONResponse: A JSON response indicating success or failure and the result of the search.
    """
    client = PostgresClient()
    # Search with department
    result = client.search_professor_department(
        first_name=first_name, last_name=last_name, department=department
    )
    # If the course title does not match dep, ex: (GESM is not a department) then search by name
    if result == None:
        result = client.search_professor_name(
            first_name=first_name, last_name=last_name
        )
    if result == None:
        # Status code 204: No Content
        return Response(status_code=204)

    return JSONResponse(content={"valid": True, "result": result}, status_code=200)


@router.post("/search-course")
def search_course(course: str = Body(..., embed=True)):
    """
    Searches for a course based on the given course name.

    Args:
        course (str): The name of the course to search for.

    Returns:
        list: A list of course objects matching the search query.
            If no matching courses are found, the list will contain a single None value.
    """
    client = PostgresClient()
    result = client.search_course(course)
    if len(result) == 0:
        return Response(status_code=204)
    return JSONResponse(content={"valid": True, "result": result}, status_code=200)
