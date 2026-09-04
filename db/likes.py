from sqlalchemy import Column, ForeignKey, DateTime, ForeignKeyConstraint, Integer, String
from sqlalchemy.sql import func

from db.base import Base

class Like (Base):
    __tablename__ = "like"

    user_id = Column("user_id", Integer, ForeignKey("user.pk_id"), primary_key=True)
    review_id = Column("review_id", Integer, ForeignKey("book_review.pk_id"), primary_key=True)
    liked_at = Column("liked_at", DateTime, nullable=False, server_default=func.now())