from pydantic import BaseModel, validator, ValidationError,EmailStr
from typing import Optional
from datetime import date


class BookSchema(BaseModel):
    title: str  
    author_id: int 
    publication_date: date 
    description : str
    image : str
    edition : str
    isbn : str
    publisher : str
    available : Optional[bool] = None  



class BooksUpdateSchema(BaseModel):
    title: Optional[str] = None  
    author: Optional[int] = None  
    publication_date : Optional[str] = None  
    available : Optional[bool] = None  



