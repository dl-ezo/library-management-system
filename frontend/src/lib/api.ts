import { Book } from '../types/book';
import { Feedback, FeedbackCreate, FeedbackCategory } from '../types/feedback';
import { RecommendationResponse } from '../types/recommendation';

// バックエンドがプレフィックスを付与するのでAPIのURLを明示的に指定
const API_URL = '/api';

export const fetchBooks = async (title?: string, borrowerName?: string): Promise<Book[]> => {
  let url = `${API_URL}/books/`;
  const params = new URLSearchParams();
  
  if (title) params.append('title', title);
  if (borrowerName) params.append('borrower_name', borrowerName);
  
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

export const createBook = async (bookData: { title: string; author?: string }): Promise<Book> => {
  const response = await fetch(`${API_URL}/books/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bookData),
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

// フィードバック関連のAPI
export const fetchFeedbacks = async (): Promise<Feedback[]> => {
  const response = await fetch(`${API_URL}/feedback/`);
  if (!response.ok) {
    throw new Error('Failed to fetch feedbacks');
  }
  return response.json();
};

export const createFeedback = async (feedback: FeedbackCreate): Promise<Feedback> => {
  const response = await fetch(`${API_URL}/feedback/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(feedback),
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to create feedback');
  }
  return response.json();
};

export const fetchFeedbackCategories = async (): Promise<FeedbackCategory[]> => {
  const response = await fetch(`${API_URL}/feedback/categories/`);
  if (!response.ok) {
    throw new Error('Failed to fetch feedback categories');
  }
  return response.json();
};

// AI書籍推薦API
export const getBookRecommendations = async (query: string): Promise<RecommendationResponse> => {
  const response = await fetch(`${API_URL}/books/recommendations/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to get book recommendations');
  }
  return response.json();
};
