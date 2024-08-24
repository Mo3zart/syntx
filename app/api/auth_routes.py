"""auth_routes.py."""

import bcrypt
from flask import Blueprint, jsonify, request

from app import db
from app.models.user_model import User

auth_blueprint = Blueprint("auth_api", __name__)


@auth_blueprint.route("/signup", methods=["POST"])
def sign_up():
    """Handle user sign-in."""
    data = request.get_json()

    # Check if the all necessary inputs are given
    if not data or "username" not in data or "email" not in data or "password" not in data:
        return jsonify(status=400, message="Missing required fields: 'username', 'email' or 'password'")

    # Check if user already exists
    if (
        User.query.filter_by(username=data["username"]).first()
        or User.query.filter_by(email=data["email"]).first()
    ):
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
    """Handle user sign-up."""
    # Extract and validate incoming JSON data
    data = request.get_json()

    # Check if the all necessary inputs are given
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
