from datetime import date
from typing import Optional
from pydantic import BaseModel

class Book:
    """本のドメインモデル"""
    
    def __init__(self, id: int, title: str, author: Optional[str] = None, borrower_name: Optional[str] = None, return_date: Optional[date] = None):
        self.id = id
        self.title = title
        self.author = author
        self.borrower_name = borrower_name
        self.return_date = return_date
    
    def borrow(self, borrower_name: str, return_date: date) -> None:
        """本を借りる"""
        if self.is_borrowed():
            raise ValueError("この本は既に貸し出されています")
        
        self.borrower_name = borrower_name
        self.return_date = return_date
    
    def return_book(self) -> None:
        """本を返却する"""
        self.borrower_name = None
        self.return_date = None
    
    def is_borrowed(self) -> bool:
        """本が貸し出されているかどうか"""
        return self.borrower_name is not None
