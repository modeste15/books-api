from sqlalchemy import Column, Text,Integer, String, ForeignKey, DateTime, Boolean, Date,Sequence
from sqlalchemy.orm import relationship,deferred
from .database import Base



metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,  Sequence('user_seq')  , primary_key=True,autoincrement=True)
    lastname = Column(String(50))
    firstname = Column(String(50))
    image = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    password = deferred(Column(String(250)))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=True)

    rents = relationship("Rent", back_populates="user")

    

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    image = Column(String(50), nullable=False)



class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)



class BookCategory(Base):
    __tablename__ = 'books_categories'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, Sequence('book_seq'),primary_key=True )
    title = Column(String(255))
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    publication_date = Column(Date)
    description = Column(Text)
    available = Column(Boolean, default=True)
    image = Column(String(250))
    edition = Column(String(250))
    isbn = Column(String(50))
    publisher = Column(String(250))

    rents = relationship("Rent", back_populates="book")





class Rent(Base):
    __tablename__ = 'rents'
    id = Column(Integer, Sequence('rent_seq') , primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    start_date = Column(Date)
    return_date = Column(Date, nullable=True)
    status = Column(Boolean, default=True)

    
    user = relationship("User", back_populates="rents")
    book = relationship("Book", back_populates="rents")
