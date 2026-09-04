from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
import os 

from db.book_reviews import BookReview
from db.users import User
from db.likes import Like
from db.base import Base

PATH = 'database/'
if (not os.path.exists(PATH)):
    os.makedirs(PATH)
 
db_url = 'sqlite:///%s/db.sqlite3' % PATH  # Database access 

engine = create_engine(db_url, echo=False)  # Connection engine 

Session = sessionmaker(bind=engine)  # Session maker instance

# Activate foreign key check
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

if not database_exists(engine.url):
    create_database(engine.url)



Base.metadata.create_all(engine)

