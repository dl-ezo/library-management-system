from datetime import date
from typing import Optional, List
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    borrower_name: Optional[str] = None
    return_date: Optional[date] = None

    class Config:
        from_attributes = True
