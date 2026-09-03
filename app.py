from flask_cors import CORS
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
# from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

# from datetime import datetime

from db import Session
from db.users import User
from logger import logger
from schemas import *

ph = PasswordHasher()
info = Info(title="Book Review API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation",
               description="Select type of documentation (Swagger, Redoc or Rapidoc)")
user_tag = Tag(name="Users",
               description="Manage users")
book_reviews_tag = Tag(name="BookReview",
               description="Manage book reviews")
likes_tag = Tag(name="Likes",
               description="Manage likes")

def normalize(string:str):
    return string.strip().upper()

@app.get('/', tags=[home_tag])
def home():
    """ Redirect user to '/openapi', where the documentation style is chosen.
    """

    return redirect('/openapi')

#region 'Users endpoints'
@app.post('/user', tags=[user_tag])
def add_user(body:UserCreateSchema):
    """Adds a new user to the database.

    Returns:
        dict: A representation of the new user
    """
    
    new_user = User(
        name = body.name.strip(),
        surname = body.surname.strip(),
        email = body.email.strip(),
        password= ph.hash(body.password)
    )

    logger.debug(f"Adding a new user: ${new_user.name} ${new_user.surname}")

    with Session() as session:
        try:
            session.add(new_user)
            session.commit()

            logger.debug(f"User {new_user.name} {new_user.surname} created successfully!")
            return show_user(new_user), 200
        except IntegrityError as err:
            logger.warning(f"IntegrityError at 'add_user': {err}")
            return {"message": "Unable to create new user!"}, 409
        except Exception as ex:
            logger.warning(f"Unable to save new user: {ex}")
            return {"message": "Unable to create new user!"}, 400

@app.get("/users", tags=[user_tag],
         responses={"200": UserListingSchema, "404": ErrorSchema})
def get_users():
    """Retrives all registered users

    Returns:
        dict: A dictionary with all registered users
    """
    logger.debug("Searching all Users...")

    with Session() as session:
        users = session.query(User).all()
        
        if not users:
            return {"users": []}, 404
        else:
            logger.debug(f"{len(users)} users found!")
            return show_users(users), 200
    

@app.get('/user', tags=[user_tag],
         responses={"200": UserViewSchema, "404": ErrorSchema})
def get_user(query: UserListingSchema):
    """Retrieves user by id, fullname and/or email address.
    
    Returns:
        dict: A dictionary with all found users
    """
    user_id = query.id
    user_fullname = query.fullname
    user_email = normalize(query.email)

    str_params = "'user_id': {user_id} | 'fullname': {user_fullname} | 'email': {user_email}"

    logger.debug(f"Searching for users with parameters: {str_params}")

    with Session() as session:
        db_query = session.query(User)

        if user_id is not None:
            db_query = db_query.filter(User.id == user_id)

        if user_fullname is not None:
                db_query = db_query.filter((User.name + " " + User.surname) == user_fullname)

        if user_email is not None:
                db_query = db_query.filter(User.normalized_email == user_email)

        users = db_query.all()

        if not users:
            logger.warning(f"No users found with filter: {str_params}")
            return {"message":f"No users found with filter: {str_params}"}, 404
        else:
            logger.debug(f"{len(users)} users found!")
            return show_users(users), 200

@app.put('/user', tags=[user_tag],
        responses={"200": UserViewSchema, "404": ErrorSchema})
def update_user(body: UserUpdateSchema):
    """Updates an user by its ID"""

    user_id = body.id

    logger.debug(f"Updating user with ID: {user_id}")

    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            return {"message": f"Us er with id {user_id} was not found"}

        try: 
            user.name = body.name
            user.surname = body.surname
            user.email = body.email 
            user.normalized_email = normalize(body.email)
            user.password = ph.hash(body.password)

            session.commit()
            return show_user(user), 200
        except Exception as ex:
            ex_msg = f"Unable to update user with id {user_id}: {ex}"
            logger.warning(ex_msg)
            return {"message": ex_msg}, 400

@app.delete('/user', tags=[user_tag],
            responses={"200":UserDeletionResultSchema, "404":ErrorSchema})
def delete_user(query:UserDeletionSchema):
    """ Removes user from database, using their id as reference."""

    user_id = query.id

    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"Couldn't find an user with id {user_id}")
            return {"message":  f"Couldn't find an user with id {user_id}"}, 404

        session.delete(user)
        session.commit()

        user_fullname = f"{user.name} {user.surname}"
        logger.debug(f"Removed user {user_id} ({user_fullname})")
        return {"message": f"Removed user {user_id} ({user_fullname})"}, 200

@app.post('/login', tags=[user_tag])
def login(body: UserLoginSchema):
    """Validates user login credentials.

        Returns:
            dict: A message output, depending on the result (success or failure).
    """
    with Session() as session:
        user_email = normalize(body.email)
        user_password = body.password.strip()

        user = session.query(User).filter(User.normalized_email == user_email).first()

        try:
            if not user:
                raise VerifyMismatchError

            ph.verify(user.password, user_password)

        except VerifyMismatchError:
            logger.warning(f"Failed login attempt for email: '{user_email}'")
            return {"message": "Invalid email/password!"}, 401
        except VerificationError as v_err:
            logger.warning(f"Failed to verify password for email '{user_email}': {v_err}")
            return {"message": "An error occurred while processing your request"}, 500

        logger.debug(f"Successful login for user with id: {user.id}")
        return {"message": "Login successful!"}, 200

#endregion
    
#region '