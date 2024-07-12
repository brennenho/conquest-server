from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.database.postgres_client import PostgresClient
from app.alerts.mail import send_watchlist_confirmation
from app.utils.helpers import formatCourseResponse
from app.utils.logger import get_logger

# This router handles all watchlist tasks

logger = get_logger(__name__)
router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.post("/add")
def add(
    section_id: str = Body(...), department: str = Body(...), email: str = Body(...)
) -> JSONResponse:
    """
    Adds a course section to the watchlist for a given email.

    Parameters:
    - section_id (str): The ID of the course section to add to the watchlist.
    - department (str): The department of the course section.
    - email (str): The email address of the user.

    Returns:
    - JSONResponse: A JSON response containing the course section information if successful,
      or an error message if unsuccessful.
    """
    try:
        PostgresClient().add_to_watchlist(section_id, department, email)

        # Send confirmation email to user
        send_watchlist_confirmation(email, section_id)

        # Get course info to return to extension
        section_info = PostgresClient().search_course_by_id(section_id)
        return JSONResponse(content=formatCourseResponse(section_info), status_code=200)

    except Exception as e:
        logger.error(f"Error adding to watchlist: {e}")
        return JSONResponse(content="failed", status_code=500)


@router.post("/delete")
def delete(section_id: str = Body(...), email: str = Body(...)) -> JSONResponse:
    """
    Deletes an email from the watchlist for a given section.

    Args:
        section_id (str): The ID of the section.
        email (str): The email to be deleted from the watchlist.

    Returns:
        JSONResponse: A JSON response indicating the success or failure of the deletion.
    """
    try:
        PostgresClient().delete_email_from_watchlist(section_id=section_id, email=email)
        return JSONResponse(content="success", status_code=200)
    except Exception as e:
        logger.error(f"Error deleting from watchlist: {e}")
        return JSONResponse(content="fail", status_code=500)


@router.post("/search")
def search(email: str = Body(...)) -> JSONResponse:
    """
    Search for watchlist sections by email.

    Args:
        email (str): The email address to search for.

    Returns:
        JSONResponse: The JSON response containing the sections found.

    Raises:
        Exception: If there is an error retrieving the watchlist.

    """
    try:
        response = PostgresClient().search_by_email(email=email)
        sections = {}
        for section in response:
            section_info = PostgresClient().search_course_by_id(section[1])
            sections[section[1]] = formatCourseResponse(section_info)
        return JSONResponse(content=sections, status_code=200)
    except Exception as e:
        logger.error(f"Error getting all watchlist: {e}")
        return JSONResponse(content=False, status_code=500)
