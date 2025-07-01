from sqlalchemy import Column, Integer, String,Float
from database import Base

# Define the Book model for the database
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    genre = Column(String)
    quantity = Column(Integer)
    price=Column(Float)
    rating=Column(Float)

class Users(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,index=True,unique=True)
    email=Column(String,index=True,unique=True)
    role=Column(String,default="user")
    hashed_password=Column(String)

