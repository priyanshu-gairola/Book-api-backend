# 📁 schemas.py
from pydantic import BaseModel,ConfigDict   # for v2
from typing import  Optional

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

# Schema for reading books from the DB
class BookResponse(BookBase):
    id: int
    quantity: int

    #model_config = ConfigDict(from_attributes=True)   v2
    class Config:   #this was in v1
        orm_mode = True #When orm_mode = True, it allows Pydantic models to read data from ORM objects directly,
                        # like instances of a SQLAlchemy model, instead of needing to convert them to dictionaries first

# Schema for updating books (partial allowed)
# class BookUpdate(BaseModel):
#     title: str | None = None
#     author: str | None = None
#     genre: str | None = None
#     quantity: int | None = None

class BookUpdate(BaseModel):
    title: Optional[str]=None
    author: Optional[str]=None
    genre: Optional[str]=None
    quantity:Optional[int]=None



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


