"""
PostTags model for representing the many-to-many relationship between posts and tags.

This module defines the `PostTags` class, which establishes the relationship between posts
and tags in the system. Each post can have multiple tags, and each tag can be associated
with multiple posts.

Classes:
    - PostTags: Represents the association between posts and tags.
"""

from app import db


class PostTags(db.Model):
    """
    Represents the association between a post and a tag in the system.

    Attributes
    ----------
    post_id : int
        The ID of the post.
    tag_id : int
        The ID of the tag.

    """

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True, nullable=False)

    def __repr__(self):
        return f"<PostTags(post_id={self.post_id}, tag_id={self.tag_id})>"

    def __init__(self, post_id, tag_id):
        """Initialize a new PostTags instance."""
        self.post_id = post_id
        self.tag_id = tag_id

    @classmethod
    def find_by_post(cls, post_id):
        """Find all tags associated with a specific post."""
        return cls.query.filter_by(post_id=post_id).all()

    @classmethod
    def find_by_tag(cls, tag_id):
        """Find all posts associated with a specific tag."""
        return cls.query.filter_by(tag_id=tag_id).all()

    def save(self):
        """Save the post-tag association to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the post-tag association from the database."""
        db.session.delete(self)
        db.session.commit()
