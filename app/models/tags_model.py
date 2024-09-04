"""
Tags model for representing tags in the system.

This module defines the `Tags` class, which represents tags within the system. It includes
attributes such as the tag name and creation timestamp. The class also provides methods for
converting tag data into a dictionary format, retrieving tags by name, and getting all tags.

Classes:
    - Tags: Represents a tag with attributes like `tag` and `created_at`.
"""

from DateTime import DateTime
from sqlalchemy import func

from app import db


class Tags(db.Model):
    """
    Represents a tag in the system.

    Attributes
    ----------
    id (int): The tag's unique identifier.
    tag (str): The name of the tag.
    created_at (DateTime): The timestamp of when the tag was created.

    """

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Tags %r>" % self.tag

    def __str__(self):
        """Return a string representation of the user."""
        return f"Tag: {self.tag}>"

    def __init__(self, tag):
        self.tag = tag

    def to_dict(self):
        return {
            "id": self.id,
            "tag_name": self.tag,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def find_by_tag(cls, tag):
        return cls.query.filter_by(tag=tag).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()
