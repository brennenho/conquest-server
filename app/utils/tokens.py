import os
import jwt

from datetime import datetime, timedelta, UTC


def validate_key(key: str) -> bool:
    return key == os.environ.get("CONQUEST_KEY")


def get_token_secret() -> str | None:
    return os.environ.get("JWT_SECRET")


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, get_token_secret(), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}


def encode_token(payload: dict) -> str:
    return jwt.encode(
        {**payload, "exp": datetime.now() + timedelta(days=1)},
        get_token_secret(),
        algorithm="HS256",
    )
