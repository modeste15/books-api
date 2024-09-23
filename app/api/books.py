from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, database

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
def create_book(title: str, author: str, publication_date: str, db: Session = Depends(get_db)):
    new_book = models.Book(title=title, author=author, publication_date=publication_date, is_available=True)
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
        (models.Book.title.contains(query)) | (models.Book.author.contains(query))
    ).all()
    return books

# Route pour obtenir les détails d'un livre spécifique par son ID
@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return book

# Route pour supprimer un livre par son ID
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    db.delete(book)
    db.commit()
    return {"detail": "Livre supprimé avec succès"}

# Route pour mettre à jour un livre (modification des détails)
@router.put("/{book_id}")
def update_book(book_id: int, title: str = None, author: str = None, publication_date: str = None, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    if title:
        book.title = title
    if author:
        book.author = author
    if publication_date:
        book.publication_date = publication_date

    db.commit()
    db.refresh(book)
    return book