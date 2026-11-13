export interface UsuarioAuth {
  id: number;
  username: string;
  full_name: string;
  email: string;
  role: 'user' | 'admin';
  disabled: boolean;
  created_at: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  full_name: string;
  email: string;
  password: string;
}

export interface MensajeResponse {
  mensaje?: string;
  message?: string;
}

export interface ApiErrorResponse {
  detail?: string | { msg: string }[];
}

export interface PaginatedResponse<T> {
  total: number;
  offset: number;
  limit: number;
  items: T[];
}