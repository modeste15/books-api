from fastapi import Request,APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import models, database
from app.validator.rent import RentValidate
from dotenv import load_dotenv
from datetime import date
from sqlalchemy.orm import joinedload




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

    rents = db.query(models.Rent).options(
        joinedload(models.Rent.user),  # Charger l'utilisateur associé
        joinedload(models.Rent.book)   # Charger le livre associé
    ).all()
    return rents

@router.post("/rents/", response_model=RentValidate)
def create_rent(rent: RentValidate, db: Session = Depends(get_db)):

    existing_rent = db.query(models.Rent).filter(
        models.Rent.user_id == rent.user_id,
        models.Rent.book_id == rent.book_id,
        models.Rent.status == True 
    ).first()

    if existing_rent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An active rent already exists for this user and book."
        )

    # livre is disponible
    book = db.query(models.Book).filter(models.Book.id == rent.book_id).first()

    if not book or not book.available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The book is currently not available for rent."
        )

    new_rent = models.Rent(
        user_id=rent.user_id,
        book_id=rent.book_id,
        start_date=date.today()
    )

    db.add(new_rent)
    db.commit()
    db.refresh(new_rent)

    # Mettre à jour la disponibilité du livre après la création de l'emprunt
    book.available = False
    db.commit()

    return new_rent



@router.get("/getback/{rent_id}")
def getback_rent(rent_id: int, db: Session = Depends(get_db)):

    rent = db.query(models.Rent).filter(models.Rent.id == rent_id).first()

    if not rent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rent not found"
        )

    if rent.return_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This rent has already been closed."
        )

    # Rendre le livre disponible
    book = db.query(models.Book).filter(models.Book.id == rent.book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    book.available = True

    rent.return_date = date.today()
    rent.status = False


    db.commit()

    return {
        "message": "Rent has been successfully closed and the book is now available.",
        "rent_id": rent.id,
        "book_title": book.title,
        "user_id": rent.user_id,
        "return_date": rent.return_date
    }