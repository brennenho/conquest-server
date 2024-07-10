from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.database.postgres_client import PostgresClient
from app.alerts.mail import send_watchlist_confirmation
from app.utils.helpers import formatCourseResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.post("/add")
def add(
    section_id: str = Body(...), department: str = Body(...), email: str = Body(...)
) -> JSONResponse:
    try:
        # send_watchlist_confirmation(email, section_id)
        PostgresClient().add_to_watchlist(section_id, department, email)
        section_info = PostgresClient().search_course_by_id(section_id)
        return JSONResponse(content=formatCourseResponse(section_info), status_code=200)
    except Exception as e:
        logger.error(f"Error adding to watchlist: {e}")
        return JSONResponse(content="fail", status_code=500)


@router.post("/delete")
def delete(section_id: str = Body(...), email: str = Body(...)) -> JSONResponse:
    try:
        PostgresClient().delete_email_from_watchlist(section_id=section_id, email=email)
        return JSONResponse(content="success", status_code=200)
    except Exception as e:
        logger.error(f"Error deleting from watchlist: {e}")
        return JSONResponse(content="fail", status_code=500)


@router.post("/search")
def get_all(email: str = Body(...)) -> JSONResponse:
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