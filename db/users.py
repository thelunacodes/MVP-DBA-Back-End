from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func

from db.base import Base

class User (Base):
    __tablename__ = "user"

    id = Column("pk_id", Integer, primary_key=True)
    name = Column("name", String(64), nullable=False)
    surname = Column("surname", String(64), nullable=False)
    email = Column("email", String(256), nullable=False)
    normalized_email = Column("normalized_email", String(256), nullable=False)
    password = Column("password", String(256), nullable=False) 
    created_at = Column("created_at", DateTime, nullable=False, server_default=func.now())
    modified_at = Column("modified_at", DateTime, nullable=True, onupdate=func.now()) 


    def __init__(self,
                 name:str, 
                 surname:str,
                 email:str, 
                 password:str,):
        """Adds a new user to the database

        Args:
            name (str): User's name
            surname (str): User's surname
            email (str): User's email address
            password (str): User's (hashed) password
        """

        self.name = name
        self.surname = surname
        self.email = email
        self.normalized_email = email.strip().upper()
        self.password = password