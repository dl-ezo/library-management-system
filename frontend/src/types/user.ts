export interface User {
  id: number;
  username: string;
  display_name: string;
  created_at: string;
}

export interface UserCreate {
  username: string;
  display_name: string;
}

export interface UserLogin {
  username: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  token_type: string;
}