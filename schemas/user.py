from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

from db.users import User

class UserSchema(BaseModel):
    """ Defines how the registered user should be represented """

    name:str
    surname:str
    email:str
    password:str
    created_at: datetime
    modified_at: Optional[datetime] = None

class UserDeletionSchema(BaseModel):
    """ Defines how the user deletion should be structured."""

    id: int

class UserSearchSchema(BaseModel):
    """ Defines how the user search should be structured """
    id:Optional[int] = None
    full_name:Optional[str] = None
    email:Optional[str]

class UserSearchResultSchema(BaseModel):
    """ Defines how the user search results should be structured """
    users: List[UserSchema]

def show_users(users: List[User]):
    """ Returns:
        dict: The representation of a user, following
        the structured in UserViewSchema
    """
    result = []
    for user in users:
        result.append({
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "created_at": user.created_at,
            "modified_at": user.modified_at
        })

    return {"users": result}

class UserViewSchema(BaseModel):
    """ Defines how the user data should be returned """

    name: str
    surname: str
    email: str
    created_at: datetime
    modified_at: Optional[datetime] = None

class UserDeletionSchema(BaseModel):
    """ 
        Defines the structure of the data returned
        after a deletion request.
    """
    message: str

def show_user(user:User):
    """Retns: 
            dict: a representation of a user, following
            the structure defined in UserViewSchema
    """

    return {
       "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "created_at": user.created_at,
        "modified_at": user.modified_at
    }