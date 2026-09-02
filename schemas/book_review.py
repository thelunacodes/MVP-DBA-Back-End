from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

from db.book_reviews import BookReview

class BookReviewSchema(BaseModel):
    """ 
        Defines how the registed book review
        should be represented.
    """

    user_id: int
    book_key: str
    review_score: float
    review_comment: Optional[str] = None
    created_at: datetime
    modified_at: Optional[datetime] = None

class UpdateSchema(BaseModel):
    """ 
        Defines how the updated review should
        be represented.
    """

    user_id: int
    book_key: str
    review_score: float
    review_comment: Optional[str] = None
    created_at: datetime
    modified_at: Optional[datetime] = None

class ReviewDeletionSchema(BaseModel):
    """ Defines how the review deletion should be structured"""

    id: int = 1

class ReviewSearchSchema(BaseModel):
    """
        Defines how the book review search
        (by user and/or book) should be structured
    """

    user_id: Optional[int] = None
    book_key: Optional[str] = None

class ReviewListingSchema(BaseModel):
    """ Defines how the book review 
        search result should be structured.
    """
    
    reviews:List[BookReview]

def show_reviews(reviews: List[BookReview]):
    """ Returns:
        dict: The representation of a book review, 
        following the structure defined in ReviewViewSchema.
    """

    result = []
    for review in reviews:
        result.append({
            "user_id": review.user_id,
            "book_key": review.book_key,
            "review_score": review.review_score,
            "review_comment": review.review_comment,
            "created_at": review.created_at,
            "modified_at": review.modified_at
        })
        
    return {"review": result}
    
class ReviewViewSchema(BaseModel):
    """ Defines how the book review
        data should be returned.
    """

    user_id:int
    book_key:str
    review_score:float
    review_comment:Optional[str]
    created_at:datetime
    modified_at:datetime 

class ReviewDeletionSchema(BaseModel):
    """ Defines the structure of the data returned 
        after a deletion request.
    """

    message:str

def show_review(review:BookReview):
    """ Returns:
            dict: a representation of a book review,
            following the structured defined in ReviewViewSchema
    """

    return {
        "user_id": review.user_id,
        "book_key": review.book_key,
        "review_score": review.review_score,
        "review_comment": review.review_comment,
        "created_at": review.created_at,
        "modified_at": review.modified_at
    }
