# 📁 crud.py
from sqlalchemy.orm import Session
import models, schemas
from auth import hash_password


# Get all books from DB
# def get_books(db: Session):
#     return db.query(models.Book).all()

#with pagination
def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


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

