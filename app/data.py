from faker import Faker
from db.database import SessionLocal
from sqlalchemy.orm import declarative_base, sessionmaker
from db.models import Base, User, Category, Author, BookCategory , Book
import os, random
from dotenv import load_dotenv
from sqlalchemy import create_engine
import datetime
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
        n = j
        user = User(
            id=index,
            lastname=fake.last_name(), 
            firstname=fake.first_name(), 
            email=fake.email(), 
            phone=fake.phone_number(),
            hashed_password='............',
            is_active=1)         

        session.add(user)
    session.commit()
    session.close()

def generate_fake_category():
    cat = ['Action', 'Adventure', 'Audiobook', 'Childrens', 'Classics', 'Dystopia', 'Fantasy', 'Fiction', 'High School', 'Historical', 'Historical Fiction', 'Literature', 'Magic', 'Middle Grade', 'Novels', 'Post Apocalyptic', 'Read For School', 'Romance', 'School', 'Science Fiction', 'Science Fiction Fantasy', 'Teen', 'Young Adult']
    for j in range(cat):
        cat = Category(
            id=j,
            name=cat[j], 
)         

        session.add(cat)
    session.commit()
    session.close() 

def generate_fake_author():
    for j in range(50):
        cat = Category(
            id=j,
            name=fake.name(), 
            image = 'test.jpg')         

        session.add(cat)
    session.commit()
    session.close() 

def generate_fake_book_category():
    for j in range(300):
        bc = Category(
            id=j,
            category_id= random.randint(1, 20), 
            boook_id = random.randint(1, 400))         

        session.add(bc)
    session.commit()
    session.close() 






    
generate_fake_users(40)
generate_fake_category()
generate_fake_author()




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
            author_id = random.randint(1, 50),
            publication_date = datetime.strptime(row[14], '%m/%d/%y').date(),
            description = row[5],
            available = 1,
            image = row[21],
            edition = row[11],
            isbn = row[7],
            publisher = row[13])         

        session.add(book)
        session.commit()
        session.close() 





generate_fake_book_category()