from app import schemas,models,crud
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,APIRouter
from app.database import get_db
from app.auth import require_admin

router=APIRouter()

@router.post("/signup",tags=["Register"], response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email/username already exists")
    return new_user

@router.post("/login",tags=["Login"])
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db, user)

#to see all users ,only admin can see
@router.get("/admin/users",response_model=list[schemas.UserResponse])
def get_all_users(db:Session=Depends(get_db),admin:models.Users=Depends(require_admin)):
    return crud.get_all_users(db)
