from fastapi import APIRouter, Body

from app.database.postgres_client import PostgresClient
from app.alerts.mail import send_watchlist_confirmation
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.post("/add")
def add(
    section_id: str = Body(...), department: str = Body(...), email: str = Body(...)
):
    try:
        # send_watchlist_confirmation(email, section_id)
        PostgresClient().add_to_watchlist(section_id, department, email)
        return {"status": "success"}
    except Exception as e:
        print(e)
    return {"status": "failed"}


@router.post("/delete")
def delete(section_id: str = Body(...), email: str = Body(...)):
    try:
        PostgresClient().delete_email_from_watchlist(section_id=section_id, email=email)
        return JSONResponse(content="success", status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content="fail", status_code=500)
