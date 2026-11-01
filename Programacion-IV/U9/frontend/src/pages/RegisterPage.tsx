import { useState } from 'react';
import { useForm } from '@tanstack/react-form';
import { Link, useNavigate } from 'react-router-dom';
import { axiosInstance } from '../api/axiosInstance';
import type { UsuarioAuth } from '../types/auth.types';

const labels = { nombre: 'Nombre', apellido: 'Apellido', email: 'Email', celular: 'Celular (opcional)', password: 'Contraseña' };
export function RegisterPage() {
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const form = useForm({
    defaultValues: { nombre: '', apellido: '', email: '', celular: '', password: '' },
    onSubmit: async ({ value }) => {
      setError('');
      try {
        await axiosInstance.post<UsuarioAuth>('/auth/register', { ...value, nombre: value.nombre.trim(), apellido: value.apellido.trim(), email: value.email.trim(), celular: value.celular.trim() || null });
        navigate('/login', { replace: true, state: { registered: true } });
      } catch (err) { setError(err instanceof Error ? err.message : 'No se pudo registrar la cuenta.'); }
    },
  });
  return <section className="mx-auto my-10 max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
    <h1 className="text-2xl font-bold">Crear cuenta</h1><p className="mt-2 mb-6 text-sm text-slate-600">Registrate para consultar el catálogo de FoodStore.</p>
    {error && <p role="alert" className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
    <form className="space-y-4" onSubmit={(event) => { event.preventDefault(); void form.handleSubmit(); }}>
      {(['nombre', 'apellido', 'email', 'celular', 'password'] as const).map((name) => <form.Field key={name} name={name}>{(field) => <label className="block text-sm font-medium">
        {labels[name]}
        <input required={name !== 'celular'} type={name === 'password' ? 'password' : name === 'email' ? 'email' : name === 'celular' ? 'tel' : 'text'} minLength={name === 'password' ? 8 : undefined} maxLength={name === 'password' ? 72 : name === 'celular' ? 20 : name === 'email' ? 254 : 80} autoComplete={name === 'password' ? 'new-password' : name === 'email' ? 'email' : name === 'nombre' ? 'given-name' : name === 'apellido' ? 'family-name' : 'tel'} value={field.state.value} onBlur={field.handleBlur} onChange={(event) => field.handleChange(event.target.value)} className="mt-1 w-full rounded-lg border border-slate-300 p-2.5" />
      </label>}</form.Field>)}
      <p className="text-xs text-slate-500">Contraseña: al menos 8 caracteres y hasta 72 bytes UTF-8.</p>
      <form.Subscribe selector={(state) => state.isSubmitting}>{(submitting) => <button disabled={submitting} className="w-full rounded-lg bg-indigo-600 p-2.5 font-semibold text-white disabled:opacity-50">{submitting ? 'Registrando...' : 'Crear cuenta'}</button>}</form.Subscribe>
    </form>
    <p className="mt-5 text-sm"><Link to="/login" className="text-indigo-700">Volver al inicio de sesión</Link></p>
  </section>;
}
