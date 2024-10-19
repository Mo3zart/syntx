from flask import Blueprint, request, jsonify

from utils.database import save_to_db
from utils.jwt_utils import token_required
from utils.validation import validate_password

profile_blueprint = Blueprint('profile_api', __name__)


@token_required
@profile_blueprint.route('/change_password', methods=['POST'])
def change_password(current_user):

    data = request.get_json()

    if not data or "new_password" not in data or "password" not in data or "confirm_new_password" not in data:
        return (
            jsonify(
                {"error": "Missing required fields: 'new_password' or 'password' or 'confirm_new_password'"},
            ),
            400,
        )

    # Check if the current password is valid
    if not current_user.check_password(data["password"]):
        return jsonify({"error": "Password validation failed"}), 400

    # Ensure the new password is provided
    if not data or 'new_password' not in data or 'confirm_new_password' not in data:
        return jsonify(
            status='400',
            message='Invalid input.',
        )

    # Validate the password
    is_valid, validation_errors = validate_password(data['new_password'])
    if not is_valid:
        return jsonify(
            status='400',
            message='Invalid password.',
            errors=validation_errors,
        )

    # Check if the new password matches the current password
    if current_user.check_password(data['new_password']):
        return jsonify(
            status='400',
            message='Password cannot be the same as the current password.',
        )

    # Hash and update the new password
    current_user.password_hash = current_user.set_password(data['new_password'])
    save_to_db(current_user)

    return jsonify(
        status='200',
        message='Password updated successfully.',
    )
