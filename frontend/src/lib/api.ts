import { Book } from '../types/book';
import { Feedback, FeedbackCreate, FeedbackCategory } from '../types/feedback';
import { apiClient } from './apiClient';

export const fetchBooks = async (title?: string, borrowerName?: string): Promise<Book[]> => {
  let url = `/books/`;
  const params = new URLSearchParams();
  
  if (title) params.append('title', title);
  if (borrowerName) params.append('borrower_name', borrowerName);
  
  if (params.toString()) {
    url += `?${params.toString()}`;
  }
  
  const response = await apiClient.get(url);
  if (!response.ok) {
    throw new Error('Failed to fetch books');
  }
  return response.json();
};

export const fetchBook = async (id: number): Promise<Book> => {
  const response = await apiClient.get(`/books/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch book');
  }
  return response.json();
};

export const createBook = async (title: string): Promise<Book> => {
  const response = await apiClient.post('/books/', { title });
  
  if (!response.ok) {
    throw new Error('Failed to create book');
  }
  return response.json();
};

export const borrowBook = async (id: number, borrowerName: string, returnDate: string): Promise<Book> => {
  const response = await apiClient.put(`/books/${id}/borrow`, {
    borrower_name: borrowerName,
    return_date: returnDate
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Failed to borrow book: ${JSON.stringify(errorData)}`);
  }
  return response.json();
};

export const returnBook = async (id: number): Promise<Book> => {
  const response = await apiClient.put(`/books/${id}/return`);
  
  if (!response.ok) {
    throw new Error('Failed to return book');
  }
  return response.json();
};

export const deleteBook = async (id: number): Promise<void> => {
  const response = await apiClient.delete(`/books/${id}`);
  
  if (!response.ok) {
    throw new Error('Failed to delete book');
  }
  return response.json();
};

// フィードバック関連のAPI
export const fetchFeedbacks = async (): Promise<Feedback[]> => {
  const response = await apiClient.get('/feedback/');
  if (!response.ok) {
    throw new Error('Failed to fetch feedbacks');
  }
  return response.json();
};

export const createFeedback = async (feedback: FeedbackCreate): Promise<Feedback> => {
  const response = await apiClient.post('/feedback/', feedback);
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to create feedback');
  }
  return response.json();
};

export const fetchFeedbackCategories = async (): Promise<FeedbackCategory[]> => {
  const response = await apiClient.get('/feedback/categories/');
  if (!response.ok) {
    throw new Error('Failed to fetch feedback categories');
  }
  return response.json();
};
