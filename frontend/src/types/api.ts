// frontend/src/types/api.ts
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
  code?: number;
  details?: any;
}

export interface ApiError {
  error: string;
  code: number;
  details?: any;
}

