from fastapi import Request,APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import models, database
from app.validator.user import UserSchema
from app.validator.auth import AuthSchema
from app.services.user_service import insert_user, verify_password,create_access_token , verify_token , get_current_user
from jose import JWTError, jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

load_dotenv()
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

# Add USER
@router.post("/")
def create_user(user: UserSchema, db: Session = Depends(get_db)):

    # Si l'utilisateur existe déjà
    user_check = db.query(models.User).filter(models.User.email == user.email).first()
    
    if user_check:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    
    user = insert_user(db, user.firstname, user.lastname , user.email, user.phone, user.password)
    return user

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
    

# ALL USERS
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# ONE USER
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

# delete user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db.delete(user)
    db.commit()
    return {"detail": "Utilisateur supprimé avec succès"}


@router.get("/detail/me")
async def read_users_me(request: Request,db: Session = Depends(get_db)):

    token = request.headers.get("Authorization")

    token = token.replace("Bearer ", "")

    #try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

    print("payload", payload )

    id: str = payload.get("sub")
    admin: str = payload.get("admin")

    print("id", id )
    print("admin", admin )


    if id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid",
        )
    user = db.query(models.User).filter(models.User.id == id).first()

    return user
    #except JWTError:
    #    raise HTTPException(
    #        status_code=status.HTTP_401_UNAUTHORIZED,
    #        detail="Token is invalid or expired",
    #    )