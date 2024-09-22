"""
Authentication routes for user sign-up and sign-in.

This module provides Flask route handlers for user authentication, including sign-up and sign-in
endpoints. Passwords are hashed using bcrypt, and email validation is performed during sign-up.

Routes:
    - POST /signup: Handle user sign-up.
    - POST /signin: Handle user sign-in.
    - POST /refresh: Handle refresh token to generate new access token.
    - POST /logout: Blacklist the token and handle user logout.
"""

import jwt
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from app.models.user_model import User
from utils.database import save_to_db
from utils.jwt_utils import (
    SECRET_KEY,
    blacklist,
    generate_refresh_token,
    generate_token,
    token_required,
)
from utils.validation import validate_email_address, validate_password

load_dotenv()

auth_blueprint = Blueprint("auth_api", __name__)


@auth_blueprint.route("/signup", methods=["POST"])
def sign_up():
    """
    Handle user sign-up.

    This route registers a new user. It performs the following steps:
        - Validates the incoming JSON data to ensure required fields are present.
        - Validates the email address format and password strength.
        - Checks if the user already exists by username or email.
        - Hashes the password using bcrypt.
        - Creates a new User object and stores it in the database.
        - Returns a success response with a 201 status code.

    Returns
    -------
    Response: A JSON response with a success message and a 201 status code if the user is created.
              If validation fails or the user already exists, it returns a 400 status code with an error message.

    """
    data = request.get_json()

    # Check if all necessary inputs are given
    if not data or "username" not in data or "email" not in data or "password" not in data:
        return jsonify(status=400, message="Missing required fields: 'username', 'email' or 'password'")

    # Check if email is valid
    if not validate_email_address(data["email"], check_mx=True):
        return jsonify(status=400, message="Invalid email address"), 400

    # Validate the password
    is_valid_password, password_errors = validate_password(data["password"])
    if not is_valid_password:
        return jsonify({"error": "Password validation failed", "details": password_errors}), 400

    # Check if user already exists
    if User.query.filter_by(username=data["username"]).first() or User.query.filter_by(email=data["email"]).first():
        return jsonify(status=400, message="User with this email or username already exists"), 400

    # Create a new User object
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        role="user",
    )

    # Add the new user to the session and commit to the database
    save_to_db(new_user)

    # Get JWT token
    access_token = generate_token(new_user.id)
    refresh_token = generate_refresh_token(new_user.id)

    # Return a success response
    return (
        jsonify({"message": "User created successfully", "access_token": access_token, "refresh_token": refresh_token}),
        201,
    )


@auth_blueprint.route("/signin", methods=["POST"])
def sign_in():
    """
    Handle user sign-in.

    This route authenticates a user by verifying their credentials and generates an access token
    and a refresh token for the session.

    Returns
    -------
    Response: A JSON response with access and refresh tokens if authentication is successful.
              If validation fails or the user is not found, it returns a 400 or 404 status code with an error message.

    """
    data = request.get_json()

    # Check if all necessary inputs are given
    if not data or "username_or_email" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields: 'username_or_email' or 'password'"}), 400

    username_or_email = data.get("username_or_email")

    # Find the user by email or username
    user = User.find_by_username_or_email(username_or_email)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verify the password using bcrypt
    if not user.check_password(data["password"]):
        return jsonify({"error": "Password validation failed"}), 400

    # Generate JWT token
    access_token = generate_token(user.id)
    refresh_token = generate_refresh_token(user.id)

    # If valid, return a success response
    return (
        jsonify(
            {
                "message": "Login successful",
                "user_id": user.id,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        ),
        200,
    )


@auth_blueprint.route("/refresh", methods=["POST"])
def refresh_token():
    """
    Refresh the access token using a valid refresh token.

    Returns
    -------
    Response: A JSON response with a new access token. If the refresh token is invalid or expired,
              it returns a 401 or 403 status code with an error message.

    """
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "Refresh token missing"}), 400

    try:
        # Decode the refresh token
        decode = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        user = User.query.filter_by(id=decode["user_id"]).first()

        if not user:
            return jsonify({"error": "Invalid refresh token"}), 401

        new_access_token = generate_token(user.id)

        return jsonify({"access_token": new_access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 403


@auth_blueprint.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    """
    Handle user logout.

    This route blacklists the user's current JWT token, preventing further use of the token.

    Parameters
    ----------
    current_user : User
        The currently authenticated user, passed by the token_required decorator.

    Returns
    -------
    Response: A JSON response confirming successful logout.

    """
    # Get the token from the request
    token = request.headers["Authorization"].split(" ")[1]

    # Add the token to the blacklist
    blacklist.add(token)

    return jsonify({"message": "Successfully logged out"}), 200
