from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

from db.likes import Like

class LikeSchema(BaseModel):
    """ Defines how the registered "like" should be represented """

    user_id:int 
    review_id:int
    liked_at:datetime

class LikeCreationSchema(BaseModel):
    """ Defines how the "like" should be structured when being
    added to the database"""

    user_id:int
    review_id:int

class LikeDeletionSchema(BaseModel):
    """ Defines how the "like" deletion should be structured."""

    user_id:int 
    review_id:int 

class LikeSearchSchema(BaseModel):
    """ Defines how the "like" search should be structured. """
    user_id:Optional[int] = None
    review_id:Optional[int] = None

class LikeListingSchema(BaseModel):
    """ Defines how the "like" search results should be structured. """
    likes: List[LikeSchema]

def show_likes(likes: List[Like]):
    """ Returns:
        dict: The representation of a like, following
        the structured in LikeViewSchema.
    """
    result = []
    for like in likes:
        result.append({
            "user_id":like.user_id,
            "review_id":like.review_id,
            "liked_at":like.liked_at
        })

    return {"likes": result}

class LikeViewSchema(BaseModel):
    """ Defines how the "like" data should be returned. """
        
    user_id: int
    review_id: int
    liked_at: datetime

class LikeDeletionResultSchema(BaseModel):
    """ 
        Defines the structure of the data returned
        after a deletion request.
    """
    message: str

def show_like(like:Like):
    """Returns: 
            dict: a representation of a "like", following
            the structure defined in LikeViewSchema.
    """

    return {
        "user_id": like.user_id,
        "review_id":like.review_id,
        "liked_at": like.liked_at
    }