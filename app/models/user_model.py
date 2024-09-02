"""
User model for representing users in the system.

This module defines the `User` class, which represents users within the system. It includes
attributes such as username, email, password hash, role, and the creation timestamp. The class
also provides methods for converting user data into a dictionary format and for representing
the user object as a string.

Classes:
    - User: Represents a user with attributes like `username`, `email`, `password_hash`, `role`,
      and `created_at`.
"""

import bcrypt
from sqlalchemy import Column, DateTime, Integer, String, func

from app import db


class User(db.Model):
    """
    Represents a user in the system.

    Attributes
    ----------
        id (int): The user's unique identifier.
        username (str): The user's username.
        email (str): The user's email address.
        password_hash (str): The hashed and salted password.
        role (str): The user's role in the system.
        created_at (datetime): The timestamp of when the user was created.

    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<User: {self.id}, {self.username}>, {self.email}>, {self.role}>, {self.created_at}>, {self.id}>"

    def __str__(self):
        """Return a string representation of the user."""
        return f"User: {self.id}, {self.username}, email: {self.email}, role: {self.role}>"

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password_hash = self.set_password(password)
        self.role = role

    def to_dict(self):
        """Return a dictionary representation of the user."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }

    def set_password(self, password):
        """Hash and set the password."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password):
        """Check the hashed password."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def update(self, **kwargs):
        """Update the user's attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    @classmethod
    def find_by_username_or_email(cls, identifier):
        """Find a user by its username or email."""
        return cls.query.filter(
            (cls.username == identifier) | (cls.email == identifier),
        ).first()
