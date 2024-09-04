"""
PostCategories model for representing the many-to-many relationship between posts and categories.

This module defines the `PostCategories` class, which establishes the relationship between posts
and categories in the system. Each post can belong to multiple categories, and each category can
have multiple posts.

Classes:
    - PostCategories: Represents the association between posts and categories.
"""

from app import db


class PostCategories(db.Model):
    """
    Represents the association between a post and a category in the system.

    Attributes
    ----------
    post_id : int
        The ID of the post.
    category_id : int
        The ID of the category.

    """

    __tablename__ = "post_categories"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), primary_key=True, nullable=False)

    def __repr__(self):
        return f"<PostCategories(post_id={self.post_id}, category_id={self.category_id})>"

    def __init__(self, post_id, category_id):
        """Initialize a new PostCategories instance."""
        self.post_id = post_id
        self.category_id = category_id

    @classmethod
    def find_by_post(cls, post_id):
        """Find all categories for a specific post."""
        return cls.query.filter_by(post_id=post_id).all()

    @classmethod
    def find_by_category(cls, category_id):
        """Find all posts associated with a specific category."""
        return cls.query.filter_by(category_id=category_id).all()

    def save(self):
        """Save the post-category association to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the post-category association from the database."""
        db.session.delete(self)
        db.session.commit()
