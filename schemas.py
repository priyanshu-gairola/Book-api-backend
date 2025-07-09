# 📁 schemas.py
from pydantic import BaseModel,ConfigDict ,Field  # for v2
from typing import  Optional
from datetime import datetime

# Shared base schema
class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    price:float=0.0
    rating:float=0.0

# Schema for creating books
class BookCreate(BookBase):
    quantity: int
    image_url:Optional[str]


# Schema for reading books from the DB
class BookResponse(BookBase):
    id: int
    quantity: int
    image_url:Optional[str]

    #model_config = ConfigDict(from_attributes=True)   v2
    class Config:   #this was in v1
        orm_mode = True #When orm_mode = True, it allows Pydantic models to read data from ORM objects directly,
                        # like instances of a SQLAlchemy model, instead of needing to convert them to dictionaries first


class BookUpdate(BaseModel):
    title: Optional[str]=None
    author: Optional[str]=None
    genre: Optional[str]=None
    quantity:Optional[int]=None
    price:Optional[float]=None
    rating:Optional[float]=None
    image_url:Optional[str]=None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role:str="user"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str


    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:str
    password:str


class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating between 1 and 5")
    content: Optional[str] = None

# For creating a review
class ReviewCreate(ReviewBase):
    pass

# For returning review data
class ReviewResponse(ReviewBase):
    id: int
    book_id: int
    user_id: int


    class Config:
        orm_mode = True

