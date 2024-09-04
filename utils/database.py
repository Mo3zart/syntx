"""
Database utility functions.

This module provides utility functions for common database operations such as saving, deleting,
and updating model instances in the database. These functions are designed to streamline
interaction with the SQLAlchemy ORM, ensuring that common tasks are handled consistently across the application.

Functions
---------
save_to_db(model)
    Save a given model instance to the database.

delete_from_db(model)
    Delete a given model instance from the database.

update(model, **kwargs)
    Update the attributes of a given model instance, with an option to update the `updated_at` timestamp.
"""

from datetime import datetime, timezone

from app import db


def save_to_db(model):
    """Save the post to the database."""
    db.session.add(model)
    db.session.commit()


def delete_from_db(model):
    """Delete the user from the database."""
    db.session.delete(model)
    db.session.commit()


def update(model, **kwargs):
    """
    Update the attributes of a given model instance.

    Parameters
    ----------
    model : db.Model
        The instance of the model to update.
    update_timestamp : bool, optional
        Whether to update the `updated_at` timestamp. Default is True.
    **kwargs : dict
        Key-value pairs of attributes to update.
        Use 'update_timestamp=False' to prevent updating the `updated_at` field.

    """
    update_timestamp = kwargs.pop("update_timestamp", True)

    for key, value in kwargs.items():
        setattr(model, key, value)
    if update_timestamp:
        model.updated_at = datetime.now(timezone.utc)
    db.session.commit()
