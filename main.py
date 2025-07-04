# 📁 main.py
from fastapi import FastAPI, Depends, HTTPException ,UploadFile,File
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine,get_db
from auth import get_current_user,require_admin
from  typing import List
from fastapi.staticfiles import StaticFiles

import shutil ,os,uuid

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API", description="Backend project with FastAPI + SQLite")

# ✅ This will make /static/images accessible from browser
app.mount("/static", StaticFiles(directory="static"), name="static")

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

#home page
@app.get("/",tags=["Welcome"])
def home():
    return {"message": "Welcome to Book API"}

# Get all books
@app.get("/books",tags=["Books"],summary="All Books",description="Get details of all books", response_model=list[schemas.BookResponse])
def read_books(db: Session = Depends(get_db),current_user: models.Users = Depends(get_current_user),
               skip:int=0,limit:int=10,  #introduced pagination also
               title:str="" ,author="",   #introduced search also
               genre:str="", min_price:float=None,max_price:float=None, # min and maxm price
                min_rating:float=None,max_rating:float=None,   #min and max ratings also
               sort_by:str=None,sort_order:str="asc"): #introduced sorting also:


    return crud.get_books(db,skip=skip,limit=limit,title=title,author=author,sort_by=sort_by,sort_order=sort_order,
                          genre=genre,min_price=min_price,max_price=max_price,
                          min_rating=min_rating,max_rating=max_rating)

# Get book by title
@app.get("/books/{title}",tags=["Books"], response_model=schemas.BookResponse)
def read_book(title: str, db: Session = Depends(get_db),current_user:models.Users=Depends(get_current_user)):
    db_book = crud.get_book_by_title(db, title)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Add book
@app.post("/books",tags=["Books"], response_model=schemas.BookResponse)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
        current_user: models.Users = Depends(require_admin)             #admin
                ):
     return crud.create_book(db, book)

# Delete book
@app.delete("/books/{title}",tags=["Books"], response_model=schemas.BookResponse)
def delete_book(title: str, db: Session = Depends(get_db),current_user:models.Users=Depends(require_admin)):
    deleted = crud.delete_book(db, title)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted

# Update book
@app.patch("/books/{title}", tags=["Books"],response_model=schemas.BookResponse)
def update_book(title: str, book: schemas.BookUpdate, db: Session = Depends(get_db),current_user:models.Users=Depends(require_admin)):
    updated = crud.update_book(db, title, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@app.post("/signup",tags=["Register"], response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return new_user

@app.post("/login",tags=["Login"])
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db, user)

#to see all users ,only admin can see
@app.get("/admim/users",response_model=list[schemas.UserResponse])
def get_all_users(db:Session=Depends(get_db),admin:models.Users=Depends(require_admin)):
    return crud.get_all_users(db)

# adding upload image route

@app.post("/upload-image")
async def upload_image(file:UploadFile=File(...)):
    if not file.content_type.startswith("image/"):  #chking file type->jpg,png
        raise HTTPException(status_code=400,detail="Invalid file type")

    ext=file.filename.split(".")[-1]   #extracted extension
    unique_filename=f"{uuid.uuid4()}.{ext}"

    file_path = os.path.join("static", "images", unique_filename) #creating path

    with open(file_path,"wb") as temp:
        shutil.copyfileobj(file.file,temp) #binary is file.file

    img_url=f"/static/images/{unique_filename}"
    return {"filename":unique_filename,"url":img_url}




