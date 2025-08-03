from app import  schemas,models,crud
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user,require_admin
from fastapi import Depends,APIRouter
from typing import List

router=APIRouter(prefix="/book")

@router.post("/{book_id}/create_review", tags=["Reviews"], response_model=schemas.ReviewResponse)
def create_review(
    book_id: int,
    review: schemas.ReviewCreate,  # ✅ This is important
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_user)):
    return crud.create_review(db=db, review=review, book_id=book_id, user_id=current_user.id)



@router.get("/{book_id}/all_reviews",tags=["Reviews"],response_model=List[schemas.ReviewResponse])
def get_reviews_for_book(book_id:int,db:Session=Depends(get_db)):    #dependecy always at last like here db

    return crud.get_reviews_for_book(db ,book_id=book_id)

