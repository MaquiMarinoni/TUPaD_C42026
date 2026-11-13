import { CartPage } from '@/features/cart/pages/CartPage';
import { CheckoutPage } from '@/features/cart/pages/CheckoutPage';
import { OrdersPage } from '@/features/orders/pages/OrdersPage';
import { AdminDashboardPage } from '@/features/orders/pages/AdminDashboardPage';
import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage, RegisterPage, AdminUsersPage } from '@/features/auth';
import { CategoriasPage } from '@/features/categories';
import { ProductsPage } from '@/features/products';
import { UnauthorizedPage } from '@/shared/components/UnauthorizedPage';
import { ProtectedRoute } from './ProtectedRoute';

export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/unauthorized" element={<UnauthorizedPage />} />

      <Route path="/categories" element={<CategoriasPage />} />
      <Route path="/products" element={<ProductsPage />} />
      <Route path="/carrito" element={<CartPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/pedidos" element={<OrdersPage />} />
      </Route>

      <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
        <Route path="/admin/resumen" element={<AdminDashboardPage />} />
        <Route path="/admin/users" element={<AdminUsersPage />} />
      </Route>

      <Route path="/categorias" element={<Navigate to="/categories" replace />} />
      <Route path="/productos" element={<Navigate to="/products" replace />} />
      <Route path="*" element={<Navigate to="/categories" replace />} />
    </Routes>
  );
}
