from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.dependencies import get_auth_header

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[get_auth_header])


@router.post("/scrape-rmp")
def scrape_rmp():
    return JSONResponse(content="success", status_code=200)
