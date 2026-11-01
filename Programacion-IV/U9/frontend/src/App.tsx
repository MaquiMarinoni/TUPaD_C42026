import { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { ProtectedRoute } from './components/ProtectedRoute';
import { CategoriasPage } from './pages/CategoriasPage';
import { ProductsPage } from './pages/ProductsPage';
import { IngredientesPage } from './pages/IngredientesPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { UnauthorizedPage } from './pages/UnauthorizedPage';
import { AdminUsersPage } from './pages/AdminUsersPage';
import { useAuthStore } from './store/authStore';

export default function App() {
  useEffect(() => { void useAuthStore.getState().checkSession(); }, []);
  return <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900"><Navbar /><main className="flex-1">
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/unauthorized" element={<UnauthorizedPage />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/categories" element={<CategoriasPage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/ingredientes" element={<IngredientesPage />} />
      </Route>
      <Route element={<ProtectedRoute allowedRoles={['admin']} />}><Route path="/admin/users" element={<AdminUsersPage />} /></Route>
      <Route path="/categorias" element={<Navigate to="/categories" replace />} />
      <Route path="/productos" element={<Navigate to="/products" replace />} />
      <Route path="*" element={<Navigate to="/categories" replace />} />
    </Routes>
  </main></div>;
}
