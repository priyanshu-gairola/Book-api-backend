from app import schemas,models,crud
from app.database import  get_db
from sqlalchemy.orm import  Session
from app.auth import get_current_user,require_admin
from fastapi import  HTTPException,Depends,APIRouter

router=APIRouter(prefix="/books")



# Get all books
@router.get("/",tags=["Books"],summary="All Books",description="Get details of all books", response_model=list[schemas.BookResponse])
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
@router.get("/{title}",tags=["Books"], response_model=schemas.BookResponse)
def read_book(title: str, db: Session = Depends(get_db),current_user:models.Users=Depends(get_current_user)):
    db_book = crud.get_book_by_title(db, title)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Add book
@router.post("/",tags=["Books"], response_model=schemas.BookResponse)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
        current_user: models.Users = Depends(require_admin)             #admin
                ):
     return crud.create_book(db, book)

# Delete book
@router.delete("/{title}",tags=["Books"], response_model=schemas.BookResponse)
def delete_book(title: str, db: Session = Depends(get_db),current_user:models.Users=Depends(require_admin)):
    deleted = crud.delete_book(db, title)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted

# Update book
@router.patch("/{title}", tags=["Books"],response_model=schemas.BookResponse)
def update_book(title: str, book: schemas.BookUpdate, db: Session = Depends(get_db),current_user:models.Users=Depends(require_admin)):
    updated = crud.update_book(db, title, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated