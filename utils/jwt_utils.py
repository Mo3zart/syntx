"""
JWT Utility Functions.

This module provides utility functions for creating and verifying JSON Web Tokens (JWTs)
to handle user authentication in the application. The tokens are signed using a secret key
and are used to securely transmit user-related information, such as `user_id`.

The utility functions include:
    - create_token: Generates a JWT token with a payload (e.g., `user_id`).
    - verify_token: Verifies the validity of the provided JWT token.

Usage:
    These functions are used in authentication routes to generate tokens during sign-in
    and verify tokens to protect routes that require authentication.

Functions:
    - create_token(user_id): Generate a JWT for the given user ID.
    - verify_token(token): Decode and verify the JWT, returning the payload if valid.
"""

import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def generate_token(user_id):
    """
    Generate a JWT token for the given user ID.

    Parameters
    ----------
    user_id : int
        The ID of the user for whom the token is generated.

    Returns
    -------
    str
        A JWT token.

    """
    exp = datetime.now(timezone.utc) + timedelta(hours=1)
    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": exp,
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return token


def verify_token(token):
    """
    Verify a JWT token and extract the user ID.

    Parameters
    ----------
    token : str
        The JWT token to be verified.

    Returns
    -------
    dict or None
        The decoded token data or None if the token is invalid or expired.

    """
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decode_token
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
