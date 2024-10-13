from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, database
from sqlalchemy.orm import joinedload
from app.validator.books import BooksUpdateSchema, BookSchema




router = APIRouter()

# Dépendance pour obtenir la session de base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour ajouter un nouveau livre
@router.post("/")
def create_book(book : BookSchema , db: Session = Depends(get_db)):

    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Route pour obtenir la liste de tous les livres
@router.get("/")
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

# Route pour rechercher un livre par son titre ou auteur
@router.get("/search/")
def search_books(query: str, db: Session = Depends(get_db)):
    books = db.query(models.Book).filter(
        (models.Book.title.contains(query)) 
    ).all()
    return books

# Route pour obtenir les détails d'un livre spécifique par son ID
@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(models.Book).options(
        joinedload(models.Book.rents).joinedload(models.Rent.user) 
    ).filter(models.Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")

    book_info = {
        "id": book.id,
        "title": book.title,
        "author_id": book.author_id,
        "publication_date": book.publication_date,
        "rents": []
    }

    # Ajouter les informations des emprunts et des utilisateurs
    for rent in book.rents:
        book_info["rents"].append({
            "rent_id": rent.id,
            "user_id": rent.user.id,
            "user_name": f"{rent.user.firstname} {rent.user.lastname}",
            "user_email": rent.user.email,
            "start_date": rent.start_date,
            "return_date": rent.return_date,
            "author": rent.author
        })

    return book_info

# Route pour supprimer un livre par son ID
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    db.delete(book)
    db.commit()
    return {"detail": "Livre supprimé avec succès"}

@router.put("/{book_id}")
def update_book(book_id: int,book_update: BooksUpdateSchema, db: Session = Depends(get_db)):
    print("ok delete")
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    if book_update.title:
        book.title = book_update.title
    if book_update.author:
        book.author = book_update.author
    if book_update.publication_date:
        book.publication_date = book_update.publication_date
    if book_update.is_available:
        book.is_available = book_update.is_available

    db.commit()
    db.refresh(book)
    return book