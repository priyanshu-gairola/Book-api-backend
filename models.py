from sqlalchemy import Column, Integer, String, Float, ForeignKey,DateTime
from sqlalchemy.orm import relationship

from database import Base


class Reviews(Base):
    __tablename__="reviews"
    id=Column(Integer,primary_key=True,index=True)
    content=Column(String,nullable=False)
    rating=Column(Float,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))



    user=relationship("Users",back_populates="reviews")
    book = relationship("Book", back_populates="reviews")


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
    image_url=Column(String,nullable=True)  #nullable to make it optional

    reviews = relationship("Reviews", back_populates="book", cascade="all, delete")


class Users(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,index=True,unique=True)
    email=Column(String,index=True,unique=True)
    role=Column(String,default="user")
    hashed_password=Column(String)

    reviews = relationship("Reviews", back_populates="user", cascade="all, delete")
    #cascade means if user deleted then all eviews from user will be deleted





