from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
import os 

from db.games import Game 
from db.base import Base

PATH = 'database/'
if (not os.path.exists(PATH)):
    os.makedirs(PATH)
 
db_url = 'sqlite:///%s/db.sqlite3' % PATH  # Acesso ao banco 

engine = create_engine(db_url, echo=False)  # Engine de conexão 

Session = sessionmaker(bind=engine)  # Instância de criador de session

if not database_exists(engine.url):
    create_database(engine.url)


Base.metadata.create_all(engine)

