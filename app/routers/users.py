from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidTokenError

from app.utils.tokens import validate_key, encode_token, decode_token
from app.alerts.manager import AlertManager
from app.database.postgres_client import PostgresClient

# This router handles all user authentication tasks

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/generate-token")
def generate_token(key: str = Body(...)):
    """
    Generates a token based on the provided key.

    Args:
        key (str): The key used to generate the token.

    Returns:
        JSONResponse: A JSON response containing the generated token if the key is valid,
        otherwise a JSON response indicating that the key is invalid.
    """
    if validate_key(key):
        return JSONResponse(
            content={"valid": True, "token": encode_token({"key": key})},
            status_code=200,
        )
    else:
        return JSONResponse(content={"valid": False, "token": ""}, status_code=401)


@router.post("/validate-token")
def validate_token(token: str = Body(...)):
    """
    Validates the given token.

    Args:
        token (str): The token to be validated.

    Returns:
        JSONResponse: A JSON response indicating whether the token is valid or not.
    """
    try:
        decode_token(token)
        return JSONResponse(content={"valid": True}, status_code=200)
    except InvalidTokenError:
        return JSONResponse(content={"valid": False}, status_code=401)


@router.post("/get-password")
async def get_password(email: str = Body(...)):
    """
    Retrieves the password for the given email address.

    Parameters:
    - email (str): The email address for which to retrieve the password.

    Returns:
    - None
    """
    manager = AlertManager()
    await manager.generate_password(email)


@router.post("/validate-password")
def validate_password(email: str = Body(...), password: str = Body(...)):
    """
    Validates the password for a given email.

    Args:
        email (str): The email address of the user.
        password (str): The password to be validated.

    Returns:
        JSONResponse: The response containing the result of password validation.

    """
    manager = AlertManager()
    return JSONResponse(
        content=manager.validate_password(email, password), status_code=200
    )
