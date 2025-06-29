import bcrypt

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()  # adds randomness
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


from datetime import datetime, timedelta
from jose import jwt  # Install: pip install python-jose

# ✅ Constants for signing JWT
SECRET_KEY = "supersecretkey"  # Keep this secret in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ✅ Create a JWT token (after successful login)
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()  # Make a copy of data (like email or id)

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})  # Add expiry time to token

    # 🔐 Sign the token with secret key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import Depends, HTTPException, status
#from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
import models

# 🧠 OAuth2 scheme reads token from header: "Authorization: Bearer <token>"
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")  # 👈 We stored email in "sub" during login
#
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#
#         user = db.query(models.Users).filter(models.Users.email == email).first()
#
#         if user is None:
#             raise HTTPException(status_code=401, detail="User not found")
#
#         return user
#
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token is invalid or expired")

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(models.Users).filter(models.Users.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")