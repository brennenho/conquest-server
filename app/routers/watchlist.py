from fastapi import APIRouter, Body

from app.database.postgres_client import PostgresClient
from app.alerts.mail import send_watchlist_confirmation

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.post("/add")
def add(
    section_id: str = Body(...), department: str = Body(...), email: str = Body(...)
):
    # send_watchlist_confirmation(email, section_id)
    PostgresClient().add_to_watchlist(section_id, department, email)
    return {"message": f"Added {email} to watchlist for {section_id}"}


@router.post("/delete")
def delete(section_id: str = Body(...), email: str = Body(...)):
    PostgresClient().delete_email_from_watchlist(section_id=section_id, email=email)
