"""
Follows model for representing the follower-followee relationship in the system.

This module defines the `Follows` class, which represents the follower-followee relationship between users.
It includes attributes such as `following_user_id`, `followed_user_id`, and `created_at`.
It also provides methods to query follower and following relationships.

Classes:
    - Follows: Represents the relationship between the follower and the followed user.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, func

from app import db


class Follows(db.Model):
    """
    Represents a follower-followee relationship in the system.

    Attributes
    ----------
        following_user_id : int
            The ID of the user who is following.
        followed_user_id : int
            The ID of the user being followed.
        created_at : datetime
            The timestamp of when the follow relationship was created.

    """

    __tablename__ = "follows"

    following_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    followed_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __init__(self, following_user_id, followed_user_id):
        """Initialize the follow relationship between two users."""
        self.following_user_id = following_user_id
        self.followed_user_id = followed_user_id

    def __repr__(self):
        return f"<Follows: following_user_id={self.following_user_id}, followed_user_id={self.followed_user_id}>"

    def to_dict(self):
        """Return a dictionary representation of the follow relationship."""
        return {
            "following_user_id": self.following_user_id,
            "followed_user_id": self.followed_user_id,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def get_followers(cls, user_id):
        """Get all users that are following a specific user."""
        return cls.query.filter_by(followed_user_id=user_id).all()

    @classmethod
    def get_following(cls, user_id):
        """Get all users that a specific user is following."""
        return cls.query.filter_by(following_user_id=user_id).all()

    @classmethod
    def is_following(cls, following_user_id, followed_user_id):
        """Check if a user is following another user."""
        return (
            cls.query.filter_by(following_user_id=following_user_id, followed_user_id=followed_user_id).first() is not None
        )

    def save(self):
        """Save the follow relationship to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the follow relationship from the database."""
        db.session.delete(self)
        db.session.commit()
