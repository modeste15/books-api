from sqlalchemy import Column, Text,Integer, String, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    
    # Relation avec le modèle Rents (emprunts)
    #rents = relationship("Rents", back_populates="users")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    publication_date = Column(Date)
    desc = Column(Text)
    available = Column(Boolean, default=True)

class Rents(Base):
    __tablename__ = 'rents'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    start_date = Column(Date)
    return_date = Column(Date, nullable=True)
    
    # Relations avec User et Book
    #user = relationship("User", back_populates="rents")
    #book = relationship("Book", back_populates="rents")
