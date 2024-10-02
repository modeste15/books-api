from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import User
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
load_dotenv()
from app.db import models, database




SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('DEBUG_MODE')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def insert_user(db: Session, firstname, lastname , email, phone, password ):
    
    password = password_hash(password)
    new_user = User(lastname=lastname, firstname=firstname, email=email, phone=phone,password=password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

def password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(db: Session,token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("sub")

        if id is None:
            raise credentials_exception

            user = db.query(models.User).filter(models.User.id == id).first()

            return user
        
    except JWTError:
        raise credentials_exception
    
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, credentials_exception)
    return username



