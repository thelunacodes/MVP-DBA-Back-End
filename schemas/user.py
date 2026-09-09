from datetime import datetime

from pydantic import BaseModel, model_validator
from typing import Optional, List

from db.users import User

class UserSchema(BaseModel):
    """ Defines how the registered user should be represented """

    name:str
    surname:str
    email:str
    normalized_email:str
    password:str
    date_of_birth: datetime
    created_at: datetime
    modified_at: Optional[datetime] = None

class UserCreateSchema(BaseModel):
    """ Defines how the user data must be structured
    during the registration process"""
    fullname: str
    email: str
    password: str
    date_of_birth: datetime

class UserUpdateSchema(BaseModel):
    """ Defines how the user update should be structured """
    id: int
    name:str
    surname:str
    email:str
    password:str

class UserLoginSchema(BaseModel):
    """ Defines how the user login should be structured."""

    email:str
    password: str

class UserIdSearchSchema(BaseModel):
    """ Defines how the user ID search should be structured."""

    id: int

class UserSearchSchema(BaseModel):
    """ Defines how the user search should be structured."""
    id:Optional[int] = None
    fullname:Optional[str] = None
    email:Optional[str] = None

    @model_validator(mode="after")
    def validate_filter(self):
        if (self.id is None and self.fullname is None and self.email is None):
            raise ValueError("You must inform, at least, one search parameter!")
        return self

class UserListingSchema(BaseModel):
    """ Defines how the user search results should be structured."""
    users: List[UserSchema]

def show_users(users: List[User]):
    """ Returns:
        dict: The representation of a user, following
        the structured in UserViewSchema.
    """
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "normalized_email": user.normalized_email,
            "date_of_birth": user.date_of_birth,
            "created_at": user.created_at,
            "modified_at": user.modified_at
        })

    return {"users": result}

class UserViewSchema(BaseModel):
    """ Defines how the user data should be returned."""

    id: int
    name: str
    surname: str
    email: str
    date_of_birth: datetime
    normalized_email: str
    created_at: datetime
    modified_at: Optional[datetime] = None

class UserDeletionResultSchema(BaseModel):
    """ 
        Defines the structure of the data returned
        after a deletion request.
    """
    message: str

def show_user(user:User):
    """Returns: 
            dict: a representation of a user, following
            the structure defined in UserViewSchema.
    """

    return {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "normalized_email": user.normalized_email,
        "date_of_birth": user.date_of_birth,
        "created_at": user.created_at,
        "modified_at": user.modified_at
    }