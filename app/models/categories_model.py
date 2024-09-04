"""
Categories model for representing categories in the system.

This module defines the `Categories` class, which represents categories within the system.
It includes attributes such as `name` and `created_at`. The class also provides methods
for converting category data into a dictionary format and querying categories.

Classes:
    - Categories: Represents a category with attributes like `name` and `created_at`.
"""

from sqlalchemy import Column, DateTime, Integer, String, func

from app import db


class Categories(db.Model):
    """
    Represents a category in the system.

    Attributes
    ----------
    id : int
        The category's unique identifier.
    name : str
        The name of the category.
    created_at : datetime
        The timestamp of when the category was created.

    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name):
        """Initialize a new category."""
        self.name = name

    def __repr__(self):
        return f"<Categories: {self.id}, {self.name}, {self.created_at}>"

    def __str__(self):
        """Return a string representation of the category."""
        return f"<Categories: {self.id}, {self.name}, Created at: {self.created_at}>"

    def to_dict(self):
        """Return a dictionary representation of the category."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def find_by_name(cls, name):
        """Find categories by name."""
        return cls.query.filter_by(name=name).all()

    @classmethod
    def get_recent_categories(cls, limit=10):
        """Get the most recently created categories."""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()

    @classmethod
    def get_all(cls):
        """
        Get all categories.

        Returns
        -------
        list
            A list of all `Categories` instances in the system.

        """
        return cls.query.all()

    def save(self):
        """Save the category to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the category from the database."""
        db.session.delete(self)
        db.session.commit()
