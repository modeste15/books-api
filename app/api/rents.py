from fastapi import Request,APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import models, database
from app.validator.rent import RentValidate
from dotenv import load_dotenv
from datetime import date



load_dotenv()




router = APIRouter()

# database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get rents
@router.get("/")
def get_rents( db: Session = Depends(get_db)):

    rents = db.query(models.Rent).all()
   
    return rents

@router.post("/rents/", response_model=RentValidate)
def create_rent(rent: RentValidate, db: Session = Depends(get_db)):

    new_rent = models.Rent(
        user_id=rent.user_id,
        book_id=rent.book_id,
        start_date=date.today()
    )
    
    db.add(new_rent)
    db.commit()
    db.refresh(new_rent)
    return new_rent