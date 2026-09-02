from datetime import datetime

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from db import Session
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Book Review API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation",
               description="Select type of documentation (Swagger, Redoc or Rapidoc)")
book_review_tag = Tag(name="Book Reviews",
               description="Mapnage book")
# game_tag = Tag(name="Game", 
#                description="Manage games registered to the database")


@app.get('/', tags=[home_tag])
def home():
    """ Redirect user to '/openapi', where the documentation style is chosen.
    """

    return redirect('/openapi')

# @app.post('/game', tags=[game_tag])
# def add_game(body:GameSchema):
#     """ Adds a new game to the database.
        
#         Returns:
#             dict: A representation of the newly added game.
#     """
    
#     game = Game(
#         imageUrl=body.imageUrl,
#         gameTitle=body.gameTitle,
#         developer=body.developer,
#         platform=body.platform,
#         gameUrl=body.gameUrl,
#         startDate=body.startDate,
#         startTime=body.startTime,
#         finishDate=body.finishDate,
#         finishTime=body.finishTime,
#         score=body.score
#     )

#     logger.debug(f"Adding a new game: '{game.gameTitle}'")

#     try:
#         session = Session()
#         session.add(game)
#         session.commit()

#         logger.debug(f"Added game: '{game.gameTitle}") 
#         return show_game(game), 200
#     except IntegrityError as err:
#         logger.warning(f"IntegrityError at 'add_game': {err}")
#         return {"message": str(err)}, 409
#     except Exception as ex:
#         logger.warning(f"Unable to save new game: {ex}")
#         return {"message": str(ex)}, 400
    
# @app.get('/games', tags=[game_tag],
#          responses={"200": GameListingSchema, "404": ErrorSchema })
# def get_games():
#     """  Retrieves all registered games. 

#     Returns:
#         dict: Dictionary with all the registered games.
#     """

#     logger.debug("Searching games...")

#     session = Session()

#     games = session.query(Game).all()

#     if not games:
#         return { "games": []}, 404
#     else:
#         logger.debug(f"{len(games)} games found!")
#         # print(games)
#         return show_games(games), 200
    
# @app.get('/game', tags=[game_tag],
#             responses={"200": GameViewSchema, "404": ErrorSchema})
# def get_game(query: GameIdSearch):
#     """ Retrieves a game by its id. 

#         Returns: 
#             dict: The game representation, if found.

#     """
#     gameId = query.id
#     logger.debug(f"Searching for '{gameId}'...")

#     session = Session()
    
#     game = session.query(Game).filter(Game.id == gameId).first()

#     if not game:
#         logger.warning(f"Game with ID {gameId} was not found.")
#         return {"message": "Couldn't fetch the game by its ID."}, 404
#     else:
#         logger.debug(f"Game found: '{game.gameTitle}'")
#         return show_game(game), 200

# @app.put('/game', tags=[game_tag],
#          responses={"200": GameViewSchema, "404": ErrorSchema})
# def update_game(body: UpdateSchema):
#     """Updates a game by its ID.
#     """

#     gameId = body.id
#     logger.debug(f"Updating game with ID: {gameId}")

#     session = Session()
#     game = session.query(Game).filter(Game.id == gameId).first()

#     if not game:
#         return {"message": "Game not found"}, 404

#     try:
#         game.imageUrl = body.imageUrl
#         game.gameTitle = body.gameTitle
#         game.developer = body.developer
#         game.platform = body.platform
#         game.gameUrl = body.gameUrl
#         game.startDate = body.startDate
#         game.startTime = body.startTime
#         game.finishDate = body.finishDate
#         game.finishTime = body.finishTime
#         game.score = body.score

#         session.commit()
#         return show_game(game), 200
#     except Exception as ex:
#         logger.warning(f"Unable to update game: {ex}")
#         return {"message": str(ex)}, 400


# @app.delete('/game', tags=[game_tag],
#             responses={"200": GameDelSchema, "404":ErrorSchema})
# def delete_game(query: GameDeletionSchema):
#     """
#         Returns:
#             dict: Dictionary with the result of the 
#                   deletion request, or an error message.
#     """

#     gameId = query.id
#     session = Session()

#     game = session.query(Game).filter(Game.id == gameId).first()

#     if not game:
#         logger.warning(f"There's no game with id {gameId}")
#         return {"message": f"There's no game with id {gameId}"}, 404

#     gameTitle = game.gameTitle

#     session.delete(game)
#     session.commit()

#     logger.debug(f"Game deleted successfully: '{gameTitle}'")

#     return {"message": f"Game '{gameTitle}' deleted."}, 200