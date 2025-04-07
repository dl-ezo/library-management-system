export interface Book {
  id: number;
  title: string;
  borrower_name: string | null;
  return_date: string | null;
}
