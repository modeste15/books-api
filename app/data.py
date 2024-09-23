from faker import Faker
from db.database import SessionLocal
from sqlalchemy.orm import declarative_base, sessionmaker
from db.models import Base, User, Book
import os, random
from dotenv import load_dotenv
from sqlalchemy import create_engine



load_dotenv() 


SQLALCHEMY_DATABASE_URL=os.getenv('SQLALCHEMY_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


fake = Faker()


#drop de la table
Base.metadata.drop_all(engine)

# Création de la table
Base.metadata.create_all(engine)

def generate_fake_users(nb):
    for _ in range(nb):
        n = random.randint(0, 999999)
        user = User(
            id=n,
            name=fake.name(), 
            email="fake.email()", 
            phone="fake.phone_number()",
            hashed_password='............',
            is_active=1)         

        session.add(user)
    session.commit()
    session.close()



def generate_fake_books(nb):
    for _ in range(nb):
        n = random.randint(0, 999999)
        book = Book(
            id = n,
            title=fake.name(),
            author=fake.name(),
            desc = fake.paragraphs(), 
            publication_date=fake.date(), 
        )
        session.add(book)
    session.commit()
    session.close()



generate_fake_users(10)
generate_fake_books(157)


