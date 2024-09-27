import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db.models import User
from main import app


SQLALCHEMY_DATABASE_URL = "oracle+oracledb://demo:demo1@localhost:1521/?service_name=ORCLPDB1"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# choisire normalement une bd de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


client = TestClient(app)


def test_read_books(test_db):
    response = client.get("/users/")
    print("*********************")
    print ("response")
    print (response)
    print("*********************")


    assert response.status_code == 200
    data = response.json()
    print("*********************")
    print ("Data")
    print (data)
    print("*********************")
    assert len(data) > 0
