"""
Posts model for representing blog posts in the system.

This module defines the `Posts` class, which represents blog posts within the system. It includes
attributes such as title, content, status, the creation timestamp, and the last updated timestamp.
The class also provides methods for converting post data into a dictionary format and for representing
the post object as a string.

Classes:
    - Posts: Represents a blog post with attributes like `title`, `content`, `status`, `created_at`,
      and `updated_at`.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app import db


class Posts(db.Model):
    """
    Represents a blog post in the system.

    Attributes
    ----------
        id (int): The post's unique identifier.
        user_id (int): The ID of the user who created the post.
        title (str): The title of the post.
        content (str): The content of the post.
        status (str): The status of the post. (e.g. draft, published).
        created_at (datetime): The creation timestamp of the post.
        updated_at (datetime): The last update timestamp of the post.

    """

    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Post: {self.id}, {self.title}, {self.content}, {self.status}, {self.created_at}, {self.updated_at}>"

    def __str__(self):
        """Return a string representation of the post."""
        return f"Post: {self.id}, {self.title}, {self.content}, Created: {self.created_at}, {self.status}, {self.updated_at}"

    def __init__(self, title, content, status):
        self.title = title
        self.content = content
        self.status = status

    def to_dict(self):
        """Return a dictionary representation of the post."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def save_to_db(self):
        """Save the post to the database."""
        db.session.add(self)
        db.session.commit()

    def update_post(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, post_id):
        return cls.query.get(post_id)

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).all()

    @classmethod
    def find_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_status(cls, status):
        return cls.query.filter_by(status=status).all()

    def publish_post(self):
        self.status = "Published"
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    @classmethod
    def search_posts(cls, keyword):
        return cls.query.filter(
            (cls.title.ilike(f"%{keyword}%"))(cls.content.ilike(f"%{keyword}%")),
        ).all()

    @classmethod
    def get_recent_posts(cls, limit=10):
        return sorted(cls.query.order_by(cls.created_at).limit(limit).all(), reverse=True)
