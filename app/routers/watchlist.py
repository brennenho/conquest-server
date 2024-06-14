from fastapi import APIRouter, Body

from app.database.postgres_client import PostgresClient

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.post("/add")
def add(
    section_id: str = Body(...), department: str = Body(...), email: str = Body(...)
):
    print(section_id, department, email)
    PostgresClient().add_to_watchlist(section_id, department, email)


@router.post("/delete")
def delete(section_id: str = Body(...), email: str = Body(...)):
    PostgresClient().delete_email_from_watchlist(section_id=section_id, email=email)
