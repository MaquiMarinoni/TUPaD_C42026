export interface UsuarioAuth {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  celular: string | null;
  roles: string[];
  deleted_at: string | null;
}
export interface LoginData { email: string; password: string }
export interface RegisterData extends LoginData { nombre: string; apellido: string; celular?: string }
export interface MensajeResponse { mensaje: string }
export interface ApiErrorResponse { detail?: string | { msg: string }[] }
export interface PaginatedResponse<T> { total: number; offset: number; limit: number; items: T[] }
