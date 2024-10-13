from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import date

app = FastAPI()

# Define a Pydantic model for the input data
class RentValidate(BaseModel):
    user_id: int
    book_id: int
