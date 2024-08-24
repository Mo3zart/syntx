"""
User profile model for representing user profiles in the system.

This module defines the `UserProfile` class, which represents user profiles associated with users
in the system. It includes attributes such as first name, last name, date of birth, profile picture URL,
bio, website URL, and the last updated timestamp. The `UserProfile` class is linked to the `User` class
via a foreign key relationship.

Classes:
    - UserProfile: Represents a user's profile with attributes like `user_id`, `first_name`,
      `last_name`, `date_of_birth`, `profile_picture_url`, `bio`, `website_url`, and `updated_at`.
"""

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app import db


class UserProfile(db.Model):
    """
    Represents a user's profile in the system.

    Attributes
    ----------
        id (int): The profile's unique identifier.
        user_id (int): The associated user's unique identifier.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        date_of_birth (date): The user's date of birth.
        profile_picture_url (str): The URL of the user's profile picture.
        bio (str): A short biography of the user.
        website_url (str): The URL of the user's website.
        updated_at (datetime): The timestamp of when the profile was last updated.

    """

    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    date_of_birth = Column(Date, nullable=True)
    profile_picture_url = Column(String(500))
    bio = Column(String(500))
    website_url = Column(String(500))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return (
            f"<UserProfile(id={self.id}, "
            f"user_id={self.user_id}, "
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}', "
            f"dob={self.date_of_birth}, "
            f"updated_at={self.updated_at})>"
        )

    def __str__(self):
        """Return a string representation of the user's profile."""
        return f"UserProfile of {self.first_name} {self.last_name}, DOB: {self.date_of_birth}"

    def __init__(
        self,
        user_id,
        first_name=None,
        last_name=None,
        date_of_birth=None,
        profile_picture_url=None,
        bio=None,
        website_url=None,
    ):
        """Initialize the user's profile."""
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.profile_picture_url = profile_picture_url
        self.bio = bio
        self.website_url = website_url
