import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage, RegisterPage, AdminUsersPage } from '@/features/auth';
import { CategoriasPage } from '@/features/categories';
import { ProductsPage } from '@/features/products';
import { IngredientesPage } from '@/features/ingredients';
import { UnauthorizedPage } from '@/shared/components/UnauthorizedPage';
import { ProtectedRoute } from './ProtectedRoute';

export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/unauthorized" element={<UnauthorizedPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/categories" element={<CategoriasPage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/ingredientes" element={<IngredientesPage />} />
      </Route>

      <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
        <Route path="/admin/users" element={<AdminUsersPage />} />
      </Route>

      <Route path="/categorias" element={<Navigate to="/categories" replace />} />
      <Route path="/productos" element={<Navigate to="/products" replace />} />
      <Route path="*" element={<Navigate to="/categories" replace />} />
    </Routes>
  );
}
