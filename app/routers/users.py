from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidTokenError

from app.utils.tokens import validate_key, encode_token, decode_token
from app.alerts.manager import AlertManager
from app.database.postgres_client import PostgresClient

router = APIRouter(prefix="/users", tags=["users"])


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


@router.post("/generate-token")
def generate_token(key: str = Body(...)):
    if validate_key(key):
        return JSONResponse(
            content={"valid": True, "token": encode_token({"key": key})},
            status_code=200,
        )
    else:
        return JSONResponse(content={"valid": False}, status_code=401)


@router.post("/validate-token")
def validate_token(token: str = Body(...)):
    try:
        decode_token(token)
        return JSONResponse(content={"valid": True}, status_code=200)
    except InvalidTokenError:
        return JSONResponse(content={"valid": False}, status_code=401)


@router.post("/get-password")
async def get_password(email: str = Body(...)):
    manager = AlertManager()
    await manager.generate_password(email)


@router.post("/validate-password")
def validate_password(email: str = Body(...), password: str = Body(...)):
    manager = AlertManager()
    return JSONResponse(
        content=manager.validate_password(email, password), status_code=200
    )
