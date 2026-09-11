from typing import Optional

from sqlalchemy import Column, Float, ForeignKey, String, DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from db.base import Base

class BookReview (Base):
    __tablename__ = "book_review"

    pk_id = Column("pk_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.pk_id"), nullable=False)
    book_key = Column("book_key", String(15), nullable=False)
    review_score = Column("review_score", Float, nullable=False)
    review_comment = Column("review_comment", String(420), nullable=True)
    created_at = Column("created_at", DateTime, nullable=False, server_default=func.now())
    modified_at = Column("modified_at", DateTime, nullable=True, onupdate=func.now()) 

    def __init__(self,
                 user_id:int, 
                 book_key:str,
                 review_score:float,
                 review_comment:Optional[str]=None):
        """Adds a new book review to the database.

        Args:
            user_id (int): The reviewer's user id.
            book_key (str): The book's identification key.
            review_score (float): Rating from 0.0 to 5.0 given by the user.
            review_comment (Optional[str]): Optional comment written by the user.
        """

        self.user_id = user_id
        self.book_key = book_key
        self.review_score = review_score
        self.review_comment = review_comment.strip() if review_comment is not None else None

    @validates("review_score")
    def validate_review_score(self, key, value):
        if not (0.0 <= value <= 5.0):
            raise ValueError(f"Review score must be a value between 0.0 and 5.0. Received: {value}")

        return value