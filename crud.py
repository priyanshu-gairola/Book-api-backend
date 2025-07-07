# 📁 crud.py
from dns.e164 import query
from sqlalchemy.orm import Session
import models, schemas
from auth import hash_password
from sqlalchemy import asc,desc


# Get all books from DB
# def get_books(db: Session):
#     return db.query(models.Book).all()

#with pagination and will add search func also
def get_books(db: Session, skip: int = 0, limit: int = 10,title:str="",author="",
              genre:str="",min_price:int=None,max_price:int=None,
              min_rating:float=None,max_rating:float=None,
              sort_by:str=None,sort_order:str="asc"):
    query=db.query(models.Book)
    if genre:
        query=query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))  # case-insensitive LIKE
    if author:
        query=query.filter(models.Book.author.ilike(f"%{author}%"))
    if min_price:
        query=query.filter(models.Book.price>=min_price)
    if max_price:
        query=query.filter(models.Book.price<=max_price)
    if min_rating:
        query=query.filter(models.Book.rating>=min_rating)
    if max_rating:
        query=query.filter(models.Book.rating<=max_rating)
    if sort_by:
        sort_column = getattr(models.Book, sort_by, None)
        if sort_column:
            if sort_order == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

    #return query.offset(skip).limit(limit).all()
    return query.offset(skip).limit(limit).all()


# Get a single book by title
def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()

# Add a new book
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())  #version 1
    #db_book = models.Book(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Delete a book
def delete_book(db: Session, title: str):
    db_book = get_book_by_title(db, title)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

# Update an existing book partially

# # ✅ PARTIAL UPDATE: Only update provided fields
# def update_book(db: Session, title: str, book_update:schemas.BookUpdate):
#     db_book = get_book_by_title(db, title)
#     if not db_book:
#         return None
#
#     # Update only fields that are not None
#     if book_update.title is not None:
#         db_book.title = book_update.title
#     if book_update.author is not None:
#         db_book.author = book_update.author
#     if book_update.genre is not None:
#         db_book.genre = book_update.genre
#     if book_update.quantity is not None:
#         db_book.quantity = book_update.quantity
#
#     db.commit()
#     db.refresh(db_book)
#     return db_book

def update_book(db: Session, title: str, updates: schemas.BookUpdate):
    db_book = get_book_by_title(db, title)
    if not db_book:
        return None

    update_data = updates.dict(exclude_unset=True)  # ← ✅ only fields user passed  version 1 pydantic
    #update_data = updates.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def create_user(db: Session, user: schemas.UserCreate):
    # Check if user already exists
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        return None

    # Hash password and create user
    hashed_pw = hash_password(user.password)
    db_user = models.Users(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException
from datetime import timedelta

def login_user(db: Session, login_data: schemas.UserLogin):
    user = db.query(models.Users).filter(models.Users.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {"sub": user.email}
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}

def get_all_users(db: Session):
    return db.query(models.Users).all()

def create_review(db:Session,user_id:int,book_id:int,review:schemas.ReviewCreate):
    # 1. Check if the book exists
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    existing = db.query(models.Reviews).filter_by(book_id=book_id, user_id=user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Review already exists.")

    new_review=models.Reviews(**review.dict(), book_id=book_id,
        user_id=user_id)   #user id and book id were not part of schema which we used for crteating review
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review

# ✅ Get all reviews for a specific book
def get_reviews_for_book(db: Session, book_id: int):
    # 1. Check if the book exists
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db.query(models.Reviews).filter(models.Reviews.book_id == book_id).all()
