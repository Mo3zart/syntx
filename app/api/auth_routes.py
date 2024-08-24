"""
Authentication routes for user sign-up and sign-in.

This module provides Flask route handlers for user authentication, including sign-up and sign-in
endpoints. Passwords are hashed using bcrypt, and email validation is performed during sign-up.

Routes:
    - POST /signup: Handle user sign-up.
    - POST /signin: Handle user sign-in.
"""

import bcrypt
from flask import Blueprint, jsonify, request

from app import db
from app.models.user_model import User
from utils.validation import validate_email_address, validate_password

auth_blueprint = Blueprint("auth_api", __name__)


@auth_blueprint.route("/signup", methods=["POST"])
def sign_up():
    """
    Handle user sign-up.

    This route registers a new user. It performs the following steps:
        - Validates the incoming JSON data to ensure required fields are present.
        - Validates the email address format and MX records.
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

    password_validation = validate_password(data.get("password", ""))

    # Check if password is valid
    if not password_validation["is_valid"]:
        return jsonify({"error": "Password validation failed", "details": password_validation["errors"]}), 400

    # Check if user already exists
    if User.query.filter_by(username=data["username"]).first() or User.query.filter_by(email=data["email"]).first():
        return jsonify(status=400, messages="User with this email or username already exists"), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Create a new User object
    new_user = User(data["username"], data["email"], hashed_password, role="user")

    # Add the new user to the session and commit to the database
    db.session.add(new_user)
    db.session.commit()

    # Return a success response
    return jsonify({"message": "User created successfully"}), 201


@auth_blueprint.route("/signin", methods=["POST"])
def sign_in():
    """
    Handle user sign-in.

    This route authenticates a user. It performs the following steps:
        - Validates the incoming JSON data to ensure required fields are present.
        - Finds the user by either username or email.
        - Verifies the provided password using bcrypt.
        - Returns a success response with the user ID if authentication is successful.

    Returns
    -------
        Response: A JSON response with a success message and the user ID if authentication is successful.
                  If validation fails or the user is not found, it returns a 400 or 404 status code with an error message.
                  If the password is incorrect, it returns a 401 status code with an error message.

    """
    # Extract and validate incoming JSON data
    data = request.get_json()

    # Check if all necessary inputs are given
    if not data or "username_or_email" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields: 'username_or_email' or 'password'"}), 400

    username_or_email = data.get("username_or_email")

    # Find the user by email or username
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email),
    ).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verify the password using bcrypt
    if not bcrypt.checkpw(data["password"].encode("utf-8"), user.password_hash.encode("utf-8")):
        return jsonify(status=410, message="error: Invalid password"), 401

    # If valid, return a success response
    return jsonify({"message": "Login successful", "user_id": user.id}), 200
