from faker import Faker
from db.database import SessionLocal
from sqlalchemy.orm import declarative_base, sessionmaker
from db.models import Base, User, Book
import os, random
from dotenv import load_dotenv
from sqlalchemy import create_engine
import datetime


load_dotenv() 

print(os.getenv('SQLALCHEMY_DATABASE_URL'))


engine = create_engine('oracle+oracledb://demo:demo1@localhost:1521/?service_name=ORCLPDB1')
Session = sessionmaker(bind=engine)
session = Session()  


fake = Faker()




#Base.metadata.drop_all(engine)


 
# Création de la table
#Base.metadata.create_all(engine)

def generate_fake_users(nb):
    for j in range(nb):
        n = random.randint(0, 99999999)
        user = User(
            id=j,
            name=fake.name(), 
            email=fake.email(), 
            phone=fake.phone_number(),
            hashed_password='............',
            is_active=1)         

        session.add(user)
    session.commit()
    session.close()



def generate_fake_books(nb):
    for j in range(nb):
        n = random.randint(0, 999999999)
        book = Book(
            id = j,
            title=fake.word(),
            author=fake.name(),
            description = fake.word(), 
            publication_date=datetime.date(1990, 5, 17))
        
        session.add(book)
    session.commit()
    session.close()



generate_fake_users(4700)
generate_fake_books(157900)
