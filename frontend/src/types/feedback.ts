export interface Feedback {
  id: number;
  title: string;
  description: string;
  category: 'bug' | 'feature' | 'improvement';
  author_name: string;
  created_at: string;
  github_issue_url?: string;
}

export interface FeedbackCreate {
  title: string;
  description: string;
  category: 'bug' | 'feature' | 'improvement';
  author_name: string;
}

export interface FeedbackCategory {
  value: string;
  label: string;
}