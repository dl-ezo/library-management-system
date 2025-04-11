import { Book } from '../types/book';

const API_URL = '';

export const fetchBooks = async (title?: string, borrowerName?: string, sortByTitle: boolean = false): Promise<Book[]> => {
  let url = `${API_URL}/books/`;
  const params = new URLSearchParams();
  
  if (title) params.append('title', title);
  if (borrowerName) params.append('borrower_name', borrowerName);
  if (sortByTitle) params.append('sort_by_title', 'true');
  
  if (params.toString()) {
    url += `?${params.toString()}`;
  }
  
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch books');
  }
  return response.json();
};

export const fetchBook = async (id: number): Promise<Book> => {
  const response = await fetch(`${API_URL}/books/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch book');
  }
  return response.json();
};

export const createBook = async (title: string): Promise<Book> => {
  const response = await fetch(`${API_URL}/books/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create book');
  }
  return response.json();
};

export const borrowBook = async (id: number, borrowerName: string, returnDate: string): Promise<Book> => {
  const response = await fetch(`${API_URL}/books/${id}/borrow`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ borrower_name: borrowerName, return_date: returnDate }),
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Failed to borrow book: ${JSON.stringify(errorData)}`);
  }
  return response.json();
};

export const returnBook = async (id: number): Promise<Book> => {
  const response = await fetch(`${API_URL}/books/${id}/return`, {
    method: 'PUT',
  });
  
  if (!response.ok) {
    throw new Error('Failed to return book');
  }
  return response.json();
};

export const deleteBook = async (id: number): Promise<void> => {
  const response = await fetch(`${API_URL}/books/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error('Failed to delete book');
  }
  return response.json();
};
