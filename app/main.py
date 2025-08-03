# 📁 main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine, get_db
from app.auth import get_current_user, require_admin
from typing import List
from fastapi.staticfiles import StaticFiles
import shutil, os, uuid

from app.routers import  books,login,reviews


# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API", description="Backend project with FastAPI + SQLite")

#  This will make /static/images accessible from browser
app.mount("/static", StaticFiles(directory="app/static"), name="static")


#home page
@app.get("/",tags=["Welcome"])
def home():
    return {"message": "Welcome to Book API"}

app.include_router(books.router)
app.include_router(login.router)
app.include_router(reviews.router)

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