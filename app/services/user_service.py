from sqlalchemy.orm import Session
from app.db.models import User

def insert_user(db: Session, firstname, lastname , email, phone, hashed_password ):
    new_user = User(lastname=lastname, firstname=firstname, email=email, phone=phone,hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user