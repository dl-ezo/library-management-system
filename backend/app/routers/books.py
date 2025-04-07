from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from app.application.services import BookService
from app.domain.models import Book as DomainBook
from app.dependencies import get_book_service

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

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

def domain_to_dto(book: DomainBook) -> Book:
    return Book(
        id=book.id,
        title=book.title,
        borrower_name=book.borrower_name,
        return_date=book.return_date
    )

@router.post("/", response_model=Book)
async def create_book(book: BookCreate, service: BookService = Depends(get_book_service)):
    domain_book = service.create_book(book.title)
    return domain_to_dto(domain_book)

@router.get("/", response_model=List[Book])
async def read_books(
    title: Optional[str] = None, 
    borrower_name: Optional[str] = None, 
    service: BookService = Depends(get_book_service)
):
    domain_books = service.get_books(title, borrower_name)
    return [domain_to_dto(book) for book in domain_books]

@router.get("/{book_id}", response_model=Book)
async def read_book(book_id: int, service: BookService = Depends(get_book_service)):
    domain_book = service.get_book(book_id)
    if not domain_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return domain_to_dto(domain_book)

@router.put("/{book_id}/borrow", response_model=Book)
async def borrow_book(
    book_id: int, 
    borrower_name: str, 
    return_date: date, 
    service: BookService = Depends(get_book_service)
):
    domain_book = service.borrow_book(book_id, borrower_name, return_date)
    if not domain_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return domain_to_dto(domain_book)

@router.put("/{book_id}/return", response_model=Book)
async def return_book(book_id: int, service: BookService = Depends(get_book_service)):
    domain_book = service.return_book(book_id)
    if not domain_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return domain_to_dto(domain_book)
