import os
import jwt

from datetime import datetime, timedelta, UTC
import random
import string


def validate_key(key: str) -> bool:
    return key == os.environ.get("ADMIN_KEY")


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


def generate_random_pass() -> str:
    """
    Generate a random one-time password.

    Returns:
        str: A 6-character alphanumeric password.
    """
    characters = string.ascii_uppercase + string.digits
    password = "".join(random.choice(characters) for _ in range(6))
    return password
