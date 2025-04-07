from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import date
from app.models.book import Book, BookCreate

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

books_db = []
book_id_counter = 1

@router.post("/", response_model=Book)
async def create_book(book: BookCreate):
    global book_id_counter
    new_book = Book(
        id=book_id_counter,
        title=book.title,
        borrower_name=None,
        return_date=None
    )
    books_db.append(new_book)
    book_id_counter += 1
    return new_book

@router.get("/", response_model=List[Book])
async def read_books(title: Optional[str] = None, borrower_name: Optional[str] = None):
    if title and borrower_name:
        return [book for book in books_db if title.lower() in book.title.lower() and 
                book.borrower_name and borrower_name.lower() in book.borrower_name.lower()]
    elif title:
        return [book for book in books_db if title.lower() in book.title.lower()]
    elif borrower_name:
        return [book for book in books_db if book.borrower_name and borrower_name.lower() in book.borrower_name.lower()]
    return books_db

@router.get("/{book_id}", response_model=Book)
async def read_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.put("/{book_id}/borrow", response_model=Book)
async def borrow_book(book_id: int, borrower_name: str, return_date: date):
    for book in books_db:
        if book.id == book_id:
            book.borrower_name = borrower_name
            book.return_date = return_date
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.put("/{book_id}/return", response_model=Book)
async def return_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            book.borrower_name = None
            book.return_date = None
            return book
    raise HTTPException(status_code=404, detail="Book not found")
