export interface Book {
  id: number;
  title: string;
  author?: string; // Add this line
  borrower_name: string | null;
  return_date: string | null;
}
