"""db_config.py."""

import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.development")


class Config:
    """General configuration."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event notifications to save memory
    SECRET_KEY = os.getenv("SECRET_KEY")  # Default value for SECRET_KEY


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True
    SQLALCHEMY_ECHO = True  # Prints SQL queries for debugging
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DB_URL")
    print(f"Database URL: {SQLALCHEMY_DATABASE_URI}")


class TestingConfig(Config):
    """Configuration for testing mode."""

    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL', 'sqlite:///test_db.sqlite')
    SQLALCHEMY_ECHO = False  # Keep this off to avoid clutter in test output


class ProductionConfig(Config):
    """Configuration for the production environment."""

    DEBUG = False
    SQLALCHEMY_ECHO = False


# Dictionary to map the environment variable to the appropriate config
config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
}
