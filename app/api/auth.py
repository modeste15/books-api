from fastapi import Request,APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import models, database
from app.validator.password import PasswordSchema
from app.validator.auth import AuthSchema
from app.services.user_service import  verify_password,create_access_token , verify_token , get_current_user
from jose import JWTError, jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from datetime import datetime
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


load_dotenv()

# database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('DEBUG_MODE')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Login USER
@router.post("/login")
def auth(user: AuthSchema, db: Session = Depends(get_db)):

    # Si l'utilisateur existe déjà
    check_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if check_user and verify_password( user.password,check_user.password):
        token = create_access_token({"sub": str(check_user.id) , "admin" : str(check_user.is_admin) })
        return {"user" : check_user.email,  "access_token": token, "token_type": "bearer"}
    else :
        raise HTTPException(status_code=400, detail="Connexion Impossible")
    

@router.post("/reset-password")
def reset_password(request: Request, new_password : PasswordSchema,db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")

    token = token.replace("Bearer ", "")
    try:
        user = verify_token()


    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    if not user:
        raise HTTPException(status_code=404, detail="Error")
    
    # Hash du nouveau mot de passe et mise à jour
    hashed_password = pwd_context.hash(new_password.password)
    user.password = hashed_password
    db.commit()
    
    return {"msg": "Password updated successfully"}