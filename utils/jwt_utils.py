"""
JWT Utility Functions.

This module provides utility functions for creating and verifying JSON Web Tokens (JWTs)
to handle user authentication in the application. The tokens are signed using a secret key
and are used to securely transmit user-related information, such as `user_id`.

The utility functions include:
    - create_token: Generates a JWT token with a payload (e.g., `user_id`).
    - verify_token: Verifies the validity of the provided JWT token.
"""

import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import jsonify, request

from app.models.user_model import User

load_dotenv()

blacklist = set()  # In-memory blacklist for testing purposes

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def generate_token(user_id, expires_in=3600):
    """
    Generate a JWT token for the given user ID.

    Parameters
    ----------
    user_id : int
        The ID of the user for whom the token is generated.
    expires_in : int, optional
        The expiration time in seconds for the token (default is 1 hour).

    Returns
    -------
    str
        A JWT token.

    """
    exp = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": exp,
        },
        SECRET_KEY,
        algorithm="HS256",
    )
    return token


def generate_refresh_token(user_id):
    """
    Generate a refresh token for the given user ID.

    Refresh tokens have a longer lifespan and are used to generate new access tokens
    when the original access token has expired.

    Parameters
    ----------
    user_id : int
        The ID of the user for whom the refresh token is generated.

    Returns
    -------
    str
        A refresh JWT token.

    """
    exp = datetime.now(timezone.utc) + timedelta(days=7)  # Refresh token lasts for 7 days
    refresh_token = jwt.encode(
        {
            "user_id": user_id,
            "exp": exp,
        },
        SECRET_KEY,
        algorithm="HS256",
    )
    return refresh_token


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


def token_required(func):
    """
    Enforce JWT token authentication for protected routes.

    This decorator function checks for the presence of a valid JWT token in the request headers.
    If the token is missing, expired, or invalid, the request is rejected with an appropriate error message.
    Otherwise, it extracts the current user from the token and passes it to the decorated route handler.

    Parameters
    ----------
    func : function
        The route handler function to be decorated.

    Returns
    -------
    function
        The decorated route handler with JWT authentication.

    """

    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        # Check for the Authorization header and extract token
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            token = auth_header.split(" ")[1] if len(auth_header.split()) > 1 else None

        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            # Decode the token to get user information
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # Check if the token is blacklisted
            if token in blacklist:
                return jsonify({"message": "Token has been blacklisted!"}), 403

            # Fetch the user from the database using the user_id in the token
            current_user = User.query.filter_by(id=data["user_id"]).first()
            if not current_user:
                return jsonify({"message": "User not found!"}), 404

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 403

        return func(current_user, *args, **kwargs)

    return decorated
