// frontend/src/types/user.ts
export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface SignupRequest {
  email: string;

  password: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  email: string;
  message: string;
}