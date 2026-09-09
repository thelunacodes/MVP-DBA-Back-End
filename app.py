from datetime import datetime

from flask_cors import CORS
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
# from urllib.parse import unquote
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

# from datetime import datetime

from db import Session
from db.book_reviews import BookReview
from db.likes import Like
from db.users import User
from logger import logger
from schemas import *
from utility_functions import build_str_params, normalize

ph = PasswordHasher()
info = Info(title="Book Review API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation",
               description="Select type of documentation (Swagger, Redoc or Rapidoc)")
user_tag = Tag(name="Users",
               description="Manage users")
book_review_tag = Tag(name="BookReview",
               description="Manage book reviews")
like_tag = Tag(name="Likes",
               description="Manage likes")

@app.get('/', tags=[home_tag])
def home():
    """ Redirect user to '/openapi', where the documentation style is chosen.
    """

    return redirect('/openapi')

#region 'Users endpoints'
@app.post('/user', tags=[user_tag])
def add_user(body:UserCreateSchema):
    """Registers a new user to the database.

    Returns:
        dict: A representation of the newly added user.
    """
    body.fullname = body.fullname.strip()

    user_name = body.fullname.split()[0]
    user_surname = "".join(body.fullname[len(user_name):])

    new_user = User(
        name = user_name,
        surname = user_surname,
        email = body.email,
        password= ph.hash(body.password.strip())
    )

    logger.debug(f"Adding a new user: ${new_user.name} ${new_user.surname}")

    with Session() as session:
        # Email validation
        userByEmail = session.query(User).filter(User.normalized_email == normalize(body.email)).first()
        
        if (userByEmail is not None):
            logger.warning(f"Email address '{new_user.email}' already in use!")
            return  {"message": "Email address already in use!"}, 409

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
    """Returns all registered users.

    Returns:
        dict: Every user registered in the database.
    """
    logger.debug("Searching all Users...")

    with Session() as session:
        users = session.query(User).all()
        
        if not users:
            return {"users": []}, 404
        
        logger.debug(f"{len(users)} users found!")
        return show_users(users), 200


@app.ger('/userbyid', tags=[user_tag],
         responses={"200": UserViewSchema, "404": ErrorSchema})
def search_user_by_id(query: UserIdSearchSchema):
    """Retrieves user by its id.
    
    Returns:
        dict: User search result.
    """ 

    logger.debug(f"Searching for user with ID {query.id}")

    with Session() as session:
        user = session.query(User).filter(User.id == query.id).first()

        if not user:
            logger.warning(f"No user found with ID {query.id}")
            return {"message":f"No user found with ID {query.id}"}, 404
        
        logger.debug(f"Found user with ID {query.id}: {user.full_name}")
        return show_user(user), 200


@app.get('/user', tags=[user_tag],
         responses={"200": UserViewSchema, "404": ErrorSchema})
def search_users(query: UserSearchSchema):
    """Lists users by id, name and/or email address.
    
    Returns:
        dict: User search results.
    """ 

    str_params = build_str_params(query)
    logger.debug(f"Searching for user records with parameters: {str_params}")

    with Session() as session:
        db_query = session.query(User)

        if query.id is not None:
            db_query = db_query.filter(User.id == query.id)

        if  query.fullname is not None:
            db_query = db_query.filter(normalize(query.fullname) in normalize(User.full_name))

        if query.email is not None:
                db_query = db_query.filter(User.normalized_email == normalize(query.email))

        users = db_query.all()

        if not users:
            logger.warning(f"No users found with filter: {str_params}")
            return {"message":f"No users found with filter: {str_params}"}, 404
        
        logger.debug(f"{len(users)} users found!")
        return show_users(users), 200

@app.put('/user', tags=[user_tag],
        responses={"200": UserViewSchema, "404": ErrorSchema})
def update_user(body: UserUpdateSchema):
    """Updates user information in the database."""

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
            ex_msg = f"Unable to update user with id {user_id}"
            logger.warning(ex_msg, ex)
            return {"message": ex_msg}, 400

@app.delete('/user', tags=[user_tag],
            responses={"200":UserDeletionResultSchema, "404":ErrorSchema})
def delete_user(query:UserIdSearchSchema):
    """ Removes an user from database."""

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
            dict: Either a "success" or "failure" message.
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
    
#region 'Book Review Endpoints' 
@app.post('/review', tags=[book_review_tag])
def add_book_review(body: ReviewCreateSchema):
    """ Registers a new book review to the database.
    
        Returns:
            dict: The newly added book review."""

    new_review = BookReview(
        user_id = body.user_id,
        book_key = body.book_key,
        review_score = body.review_score,
        review_comment = body.review_comment
    )

    with Session() as session:
        try:
            session.add(new_review)
            session.commit()

            logger.debug(f"Registed new book review! (User ID={new_review.user_id} | Book KEY={new_review.book_key})")
            return show_review(new_review), 200
        except IntegrityError as err:
            logger.warning(f"Integrity Error at add_book_review: {err}")
            return { "message": "Couldn't add new book review!"}, 409
        except Exception as ex: 
            logger.warning(f"Unable to create new book review: {ex}")
            return { "message": "Couldn't add new book review!"}, 400
        
@app.get("/reviews", tags=[book_review_tag],
         responses={"200": ReviewListingSchema, "404": ErrorSchema})
def get_reviews():
    """ Returns all registered book reviews.
    
        Returns:
            dict: Every book review registered in the database."""

    logger.debug("Searching all Book Reviews...")

    with Session() as session:
        reviews = session.query(BookReview).all()

        if not reviews:
            return { "reviews: ", []}, 404

        logger.debug(f"{len(reviews)} found!")
        return show_reviews(reviews)

@app.get('/review', tags=[book_review_tag],
    responses={"200": ReviewViewSchema, "404": ErrorSchema})
def search_reviews(query: ReviewSearchSchema):
    """Lists book reviews by ID, user ID, book key, 
    min and max review scores and/or comment excerpt.
    
    Returns:
        dict: Book review search results.
    """ 

    str_params = build_str_params(query)

    logger.debug(f"Searching for book review records with parameters: {str_params}")

    with Session() as session:
        db_query = session.query(BookReview)

        if query.pk_id is not None:
            db_query = db_query.filter(BookReview.pk_id == query.pk_id)
        
        if query.user_id is not None:
            db_query = db_query.filter(BookReview.user_id == query.user_id)

        if  query.book_key is not None:
            db_query = db_query.filter(BookReview.book_key == query.book_key)

        if  query.min_score is not None:
            db_query = db_query.filter(BookReview.review_score >= query.min_score)

        if  query.max_score is not None:
            db_query = db_query.filter(BookReview.review_score <= query.max_score)

        if  query.comment is not None:
            db_query = db_query.filter(func.upper(BookReview.review_comment).contains(normalize(query.comment)))

        reviews = db_query.all()
    
        if not reviews:
            logger.warning(f"No book reviews found with filter: {str_params}")
            return {"message":f"No book reviews found with filter: {str_params}"}, 404
        
        logger.debug(f"{len(reviews)} reviews found!")
        return show_reviews(reviews), 200

@app.put('/review', tags=[book_review_tag],
        responses={"200": ReviewViewSchema, "404": ErrorSchema})
def update_review(body: ReviewUpdateSchema):
    """Updates user information in the database."""

    review_id = body.pk_id

    logger.debug(f"Updating book review with ID {review_id}")

    with Session() as session:
        review = session.query(BookReview).filter(BookReview.pk_id == review_id).first()

        if not review:
            return {"message": f"Book review with ID {review_id} was not found"}

        try: 
            review.user_id = body.user_id
            review.book_key= body.book_key
            review.review_comment = body.review_comment
            review.review_score = body.review_score

            session.commit()
            return show_review(review), 200
        except Exception as ex:
            ex_msg = f"Unable to update book review with ID {review_id}"
            logger.warning(ex_msg, ex)
            return {"message": ex_msg}, 400

@app.delete('/review', tags=[book_review_tag],
            responses={"200":ReviewDeletionResultSchema, "404":ErrorSchema})
def delete_review(query:ReviewDeletionSchema):
    """ Removes a book review from database."""

    review_id = query.pk_id

    with Session() as session:
        review = session.query(BookReview).filter(BookReview.pk_id == review_id).first()

        if not review:
            logger.warning(f"Couldn't find a book review with ID {review_id}")
            return {"message":  f"Couldn't find book review with ID {review_id}"}, 404

        session.delete(review)
        session.commit()

        logger.debug(f"Removed book review with ID {review_id}")
        return {"message": f"Removed user book review with ID {review_id}"}, 200

#endregion

#region 'likes region'
@app.put('/like', tags=[like_tag])
def add_like(body: LikeCreationSchema):
    """ Registers a new 'like' to the database.
    
        Returns:
            dict: The newly added 'like'."""

    new_like = Like(
        user_id = body.user_id,
        review_id = body.review_id
    )

    with Session() as session:
        try:
            session.add(new_like)
            session.commit()

            logger.debug(f"Registed new like! (User ID={new_like.user_id} | Review ID={new_like.review_id})")
            return show_like(new_like), 200
        except IntegrityError as err:
            logger.warning(f"Integrity Error at add_like: {err}")
            return { "message": "Couldn't add new 'like'!"}, 409
        except Exception as ex: 
            logger.warning(f"Unable to create new 'like': {ex}")
            return { "message": "Couldn't add new 'like'!"}, 400
        
@app.get("/likes", tags=[like_tag],
         responses={"200": LikeListingSchema, "404": ErrorSchema})
def get_likes():
    """ Returns all registered 'likes'.
    
        Returns:
            dict: Every 'like' in the database."""

    logger.debug("Searching all likes...")

    with Session() as session:
        likes = session.query(Like).all()

        if not likes:
            return { "likes: ", []}, 404

        logger.debug(f"{len(likes)} found!")
        return show_likes(likes)

@app.get('/like', tags=[like_tag],
    responses={"200": LikeViewSchema, "404": ErrorSchema})
def search_likes(query: LikeSearchSchema):
    """Lists 'likes' either by user ID or review ID
    
    Returns:
        dict: 'like' search results.
    """ 

    str_params = build_str_params(query)

    logger.debug(f"Searching for 'like' records with parameters: {str_params}")

    with Session() as session:
        db_query = session.query(Like)

        if query.user_id is not None:
            db_query = db_query.filter(Like.user_id == query.user_id)

        if query.review_id is not None:
            db_query = db_query.filter(Like.review_id == query.review_id)

        likes = db_query.all()
    
        if not likes:
            logger.warning(f"No 'likes' found with filter: {str_params}")
            return {"message":f"No 'likes' found with filter: {str_params}"}, 404
        
        logger.debug(f"{len(likes)} likes found!")
        return show_likes(likes), 200

@app.delete('/like', tags=[like_tag],
            responses={"200":LikeDeletionResultSchema, "404":ErrorSchema})
def delete_like(query:LikeDeletionSchema):
    """ Removes a 'like' record from database"""

    user_id = query.user_id
    review_id = query.review_id

    with Session() as session:
        like = session.query(Like).filter(Like.user_id == user_id and Like.review_id == review_id).first()

        if not like:
            logger.warning(f"Couldn't find a 'like' with user_id {user_id} and review_id {review_id}")
            return {"message":  f"Couldn't find a 'like' with user_id {user_id} and review_id {review_id}"}, 404

        session.delete(like)
        session.commit()

        logger.debug(f"Removed 'like' with user_id {user_id} and review_id {review_id}")
        return {"message": f"Removed user 'like' with user_id {user_id} and review_id {review_id}"}, 200