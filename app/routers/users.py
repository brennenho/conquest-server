from fastapi import APIRouter, Body
from jwt.exceptions import InvalidTokenError

from app.utils.tokens import validate_key, encode_token, decode_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/generate-token")
def generate_token(key: str = Body(...)):
    if validate_key(key):
        return {"valid": True, "token": encode_token({"key": key})}
    else:
        return {"valid": False}


@router.post("/validate-token")
def validate_token(token: str = Body(...)):
    try:
        decode_token(token)
        return {"valid": True}
    except InvalidTokenError:
        return {"valid": False}
