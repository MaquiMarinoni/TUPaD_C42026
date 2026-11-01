import { useState } from 'react';
import { useForm } from '@tanstack/react-form';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import type { LoginData } from '../types/auth.types';

export function LoginPage() {
  const { user, loading, login } = useAuthStore();
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const form = useForm({
    defaultValues: { email: '', password: '' } as LoginData,
    onSubmit: async ({ value }) => {
      setError('');
      try { await login(value.email.trim(), value.password); navigate('/categories', { replace: true }); }
      catch (err) { setError(err instanceof Error ? err.message : 'No se pudo iniciar sesión.'); }
    },
  });
  if (user && !loading) return <Navigate to="/categories" replace />;
  return <section className="mx-auto my-12 max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
    <h1 className="text-2xl font-bold">Iniciar sesión</h1><p className="mt-2 mb-6 text-sm text-slate-600">Ingresá a FoodStore con tu email y contraseña.</p>
    {location.state?.registered && <p role="status" className="mb-4 text-sm text-emerald-700">Cuenta creada. Ya podés iniciar sesión.</p>}
    {error && <p role="alert" className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
    <form className="space-y-4" onSubmit={(event) => { event.preventDefault(); void form.handleSubmit(); }}>
      {(['email', 'password'] as const).map((name) => <form.Field key={name} name={name}>{(field) => <label className="block text-sm font-medium">
        {name === 'email' ? 'Email' : 'Contraseña'}
        <input required type={name === 'email' ? 'email' : 'password'} autoComplete={name === 'email' ? 'email' : 'current-password'} value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} className="mt-1 w-full rounded-lg border border-slate-300 p-2.5" />
      </label>}</form.Field>)}
      <form.Subscribe selector={(state) => state.isSubmitting}>{(submitting) => <button disabled={submitting || loading} className="w-full rounded-lg bg-indigo-600 p-2.5 font-semibold text-white disabled:opacity-50">{submitting ? 'Ingresando...' : 'Ingresar'}</button>}</form.Subscribe>
    </form>
    <p className="mt-5 text-sm text-slate-600">¿No tenés cuenta? <Link className="font-medium text-indigo-700" to="/register">Registrate</Link></p>
  </section>;
}
