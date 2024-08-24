"""auth_routes.py."""

import hashlib

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

    # Hash the password
    hashed_password = hashlib.sha256(data["password"].encode("utf-8")).hexdigest()

    # Create a new User object
    new_user = User(data["username"], data["email"], hashed_password)

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

    # Find the user by email or username
    user = User.query.filter(
        (User.username == data["username_or_email"]) | (User.email == data["username_or_email"]),
    ).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Hash the incoming password
    hashed_password = hashlib.sha256(data["password"].encode("utf-8")).hexdigest()

    # Verify the password
    if user.password_hash != hashed_password:
        return jsonify({"error": "Invalid password"}), 401

    # If valid, return a success response (you might generate a token here)
    # Placeholder for token generation or any other login process
    # For simplicity, we're just returning a success message here
    return jsonify({"message": "Login successful", "user_id": user.id}), 200
