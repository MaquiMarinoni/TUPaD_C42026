export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
}

// Tipo para el formulario de creación (sin id, ya que lo genera el backend)
export type CategoriaFormData = Omit<Categoria, 'id'>;