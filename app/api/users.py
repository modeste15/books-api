from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, database
from app.validator.user import UserSchema
from app.services.user_service import insert_user



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
    
    
    user = insert_user(db, user.firstname, user.lastname , user.email, user.phone, user.hashed_password)


    return user

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