from jwt.exceptions import InvalidTokenError
from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.tokens import decode_token


def get_auth_header(
    request: Request,
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> None:
    """
    Retrieves the authorization header from the request and validates the token.

    Args:
        request (Request): The incoming request object.
        authorization (HTTPAuthorizationCredentials, optional):
            The authorization credentials extracted from the request header.

    Raises:
        HTTPException: If the authorization header is missing or the token is invalid.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    try:
        result = decode_token(authorization.credentials)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
