"""__inti__.py."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from db_config import config_by_name

# Initialize the database
db = SQLAlchemy()


def create_app(config_name="dev"):
    """Initialize the Flask application."""
    app = Flask(__name__)

    # Load the config from the object in db_config.py
    app.config.from_object(config_by_name[config_name])

    # Initialize the extensions
    db.init_app(app)

    return app
