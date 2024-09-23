"""__inti__.py."""

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from db_config import config_by_name

# Initialize the database
db = SQLAlchemy()


def create_app(config_name="dev"):
    """Initialize the Flask application."""
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Load the config from the object in db_config.py
    app.config.from_object(config_by_name[config_name])

    # Initialize the extensions
    db.init_app(app)

    # Initialize Swagger
    if config_name == "dev":
        Swagger(app)

    # Import and register blueprints
    from app.api.auth_routes import auth_blueprint

    # from app.models.user_model import User
    # from app.models.user_profile_model import UserProfile

    app.register_blueprint(auth_blueprint, url_prefix="/api/authentication")

    return app
