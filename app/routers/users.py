from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidTokenError

from app.utils.tokens import validate_key, encode_token, decode_token
from app.alerts.manager import AlertManager

router = APIRouter(prefix="/users", tags=["users"])


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
