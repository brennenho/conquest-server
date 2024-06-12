from jwt.exceptions import InvalidTokenError
from fastapi import Request, Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.tokens import decode_token


def get_auth_header(
    request: Request,
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> None:
    if not authorization:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    try:
        result = decode_token(authorization.credentials)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
