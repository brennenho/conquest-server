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
    """
    Decode a JSON Web Token (JWT) and return the decoded payload.

    Args:
        token (str): The JWT to decode.

    Returns:
        dict: The decoded payload as a dictionary.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        return jwt.decode(token, get_token_secret(), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}


def encode_token(payload: dict) -> str:
    """
    Encodes the given payload into a JSON Web Token (JWT) string that expires in 24 hours.

    Args:
        payload (dict): The payload to be encoded into the token.

    Returns:
        str: The encoded JWT string.
    """
    return jwt.encode(
        {**payload, "exp": datetime.now() + timedelta(days=1)},
        get_token_secret(),
        algorithm="HS256",
    )


def generate_random_pass() -> str:
    """
    Generate a random one-time password.

    Returns:
        str: A 5-character numeric password.
    """
    characters = string.digits
    password = "".join(random.choice(characters) for _ in range(5))
    return password
