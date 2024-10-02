from faker import Faker
from db.database import SessionLocal
from sqlalchemy.orm import declarative_base, sessionmaker
from db.models import Base, User, Category, Author, BookCategory , Book
import os, random
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime
import csv
import random





load_dotenv() 

print(os.getenv('SQLALCHEMY_DATABASE_URL'))


engine = create_engine('oracle+oracledb://demo:demo1@localhost:1521/?service_name=ORCLPDB1')
Session = sessionmaker(bind=engine)
session = Session()  


fake = Faker()
def generate_fake_users(nb):
    for j in range(nb):
        user = User(
            id=j,
            lastname=fake.last_name(), 
            firstname=fake.first_name(), 
            email=fake.email(), 
            password='............',
            is_active=1)         

        session.add(user)
    session.commit()
    session.close()

def generate_fake_category():
    cat = ['Action', 'Adventure', 'Audiobook', 'Childrens', 'Classics', 'Dystopia', 'Fantasy', 'Fiction', 'High School', 'Historical', 'Historical Fiction', 'Literature', 'Magic', 'Middle Grade', 'Novels', 'Post Apocalyptic', 'Read For School', 'Romance', 'School', 'Science Fiction', 'Science Fiction Fantasy', 'Teen', 'Young Adult']
    
    for index, j in enumerate(cat):
        cat = Category(
            id=index,
            name=j )         

        session.add(cat)
    session.commit()
    session.close() 

def generate_fake_author():
    for j in range(50):
        cat = Author(
            id=j,
            name=fake.name(), 
            image = 'test.jpg')         

        session.add(cat)
    session.commit()
    session.close() 

def generate_fake_book_category():
    for j in range(2):
        bc = BookCategory(
            id=j+4,
            category_id= random.randint(1, 20), 
            book_id = random.randint(10, 350))         

        session.add(bc)
    session.commit()
    session.close() 



def upload_book (): 
    with open('books.csv', mode='r', encoding='utf-8') as file:
        # Créer un lecteur CSV
        csv_reader = csv.reader(file)
        
        # Boucle sur chaque ligne du fichier CSV

        for index, row in enumerate(csv_reader, start=2):
            if index > 400:
                break
            book = Book (
                id=index,
                title = row[1],
                author_id = random.randint(1, 49),
                publication_date = fake.date_between(start_date='-10y', end_date='today'),
                description = row[5],
                available = 1,
                image = row[21],
                edition = row[11],
                isbn = row[7],
                publisher = row[13])         

            session.add(book)
            session.commit()
            session.close() 




generate_fake_users(40)
#generate_fake_category()
#generate_fake_author()
upload_book()

generate_fake_book_category()



