export interface BookRecommendation {
  title: string;
  author: string;
  amazon_url: string;
  recommendation_reason: string;
}

export interface RecommendationRequest {
  query: string;
}

export interface RecommendationResponse {
  recommendations: BookRecommendation[];
}