from sqlalchemy import Column, ForeignKey, DateTime, ForeignKeyConstraint, Integer, String
from sqlalchemy.sql import func

from db.base import Base

class Like (Base):
    __tablename__ = "like"

    user_id = Column("user_id", Integer, primary_key=True)
    book_key = Column("book_key", String(12),  primary_key=True)
    liked_at = Column("liked_at", DateTime, nullable=False, server_default=func.now())

    # Referenciar a chave composta da tabela 'book_review'
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "book_key"],
            ["book_review.user_id", "book_review.book_key"]
        ),
    )