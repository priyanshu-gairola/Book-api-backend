# 📁 main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine,get_db
from auth import get_current_user


# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API", description="Backend project with FastAPI + SQLite")

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

#home page
@app.get("/")
def home():
    return {"message": "Welcome to Book API"}

# Get all books
@app.get("/books", response_model=list[schemas.BookResponse])
def read_books(db: Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return crud.get_books(db)

# Get book by title
@app.get("/books/{title}", response_model=schemas.BookResponse)
def read_book(title: str, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db, title)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Add book
@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

# Delete book
@app.delete("/books/{title}", response_model=schemas.BookResponse)
def delete_book(title: str, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, title)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted

# Update book
@app.patch("/books/{title}", response_model=schemas.BookResponse)
def update_book(title: str, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    updated = crud.update_book(db, title, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return new_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db, user)


# from fastapi.openapi.utils import get_openapi
#
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title=app.title,
#         version="1.0",
#         description=app.description,
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT"
#         }
#     }
#     for path in openapi_schema["paths"].values():
#         for operation in path.values():
#             operation["security"] = [{"BearerAuth": []}]
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
# app.openapi_schema = None  # 🔁 Force FastAPI to rebuild schema
# app.openapi = custom_openapi
#


