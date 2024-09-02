"""
Comments model for representing comments on posts in the system.

This module defines the `Comments` class, which represents comments within the system. It includes
attributes such as content, user ID, post ID, parent comment ID, and the creation timestamp. The class
also provides methods for converting comment data into a dictionary format and for retrieving comments
based on various criteria.

Classes:
    - Comments: Represents a comment with attributes like `content`, `user_id`, `post_id`, `parent_comment_id`,
      and `created_at`.
"""

from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship

from app import db


class Comments(db.Model):
    """
    Represents a comment in the system.

    Attributes
    ----------
    id : int
        The comment's unique identifier.
    content : str
        The content of the comment.
    user_id : int
        The ID of the user who posted the comment.
    post_id : int
        The ID of the post the comment is associated with.
    parent_comment_id : int, optional
        The ID of the parent comment if this comment is a reply to another comment.
    created_at : datetime
        The timestamp of when the comment was created.

    """

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    created_at = db.Column(DateTime(timezone=True), default=func.now(), nullable=False)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    parent_comment = relationship("Comments", remote_side=[id])

    def __init__(self, content, user_id, post_id, parent_comment_id):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id
        self.parent_comment_id = parent_comment_id

    def __repr__(self):
        return (
            f"<Comment: id={self.id}, content='{self.content}', user_id={self.user_id}, "
            f"post_id={self.post_id}, parent_comment_id={self.parent_comment_id}, created_at={self.created_at}>"
        )

    def __str__(self):
        """Return a string representation of the comment."""
        return f"Comment: {self.id}, {self.content}"

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "parent_comment_id": self.parent_comment_id,
            "created_at": self.created_at,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_content(self, new_content):
        self.content = new_content
        db.session.commit()

    @classmethod
    def get_replies(cls, comment_id):
        """Retrieve all replies to a specific comment."""
        return cls.query.filter_by(parent_comment_id=comment_id).all()

    @classmethod
    def count_comments_by_post(cls, post_id):
        """Count the number of comments associated with a specific post."""
        return cls.query.filter_by(post_id=post_id).count()

    @classmethod
    def count_comments_by_user(cls, user_id):
        """Count the number of comments made by a specific user."""
        return cls.query.filter_by(user_id=user_id).count()
