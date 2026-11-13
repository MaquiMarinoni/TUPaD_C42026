import { useState } from 'react';
import { useForm } from '@tanstack/react-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import type { RegisterData } from '../types/auth.types';

export function RegisterPage() {
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { register } = useAuth();

  const form = useForm({
    defaultValues: {
      username: '',
      full_name: '',
      email: '',
      password: '',
    } as RegisterData,

    onSubmit: async ({ value }) => {
      setError('');

      try {
        await register({
          username: value.username.trim(),
          full_name: value.full_name.trim(),
          email: value.email.trim(),
          password: value.password,
        });

        navigate('/login', {
          replace: true,
          state: { registered: true },
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'No se pudo registrar la cuenta.');
      }
    },
  });

  return (
    <section className="mx-auto my-10 max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
      <h1 className="text-2xl font-bold">Crear cuenta</h1>

      <p className="mt-2 mb-6 text-sm text-slate-600">
        Registrate para comprar en Food Store.
      </p>

      {error && (
        <p role="alert" className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      )}

      <form
        className="space-y-4"
        onSubmit={(event) => {
          event.preventDefault();
          void form.handleSubmit();
        }}
      >
        <form.Field name="username">
          {(field) => (
            <label className="block text-sm font-medium">
              Usuario
              <input
                required
                type="text"
                autoComplete="username"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(event) => field.handleChange(event.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-300 p-2.5"
              />
            </label>
          )}
        </form.Field>

        <form.Field name="full_name">
          {(field) => (
            <label className="block text-sm font-medium">
              Nombre completo
              <input
                required
                type="text"
                autoComplete="name"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(event) => field.handleChange(event.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-300 p-2.5"
              />
            </label>
          )}
        </form.Field>

        <form.Field name="email">
          {(field) => (
            <label className="block text-sm font-medium">
              Email
              <input
                required
                type="email"
                autoComplete="email"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(event) => field.handleChange(event.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-300 p-2.5"
              />
            </label>
          )}
        </form.Field>

        <form.Field name="password">
          {(field) => (
            <label className="block text-sm font-medium">
              Contraseña
              <input
                required
                minLength={8}
                maxLength={72}
                type="password"
                autoComplete="new-password"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(event) => field.handleChange(event.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-300 p-2.5"
              />
            </label>
          )}
        </form.Field>

        <form.Subscribe selector={(state) => state.isSubmitting}>
          {(submitting) => (
            <button
              disabled={submitting}
              className="w-full rounded-lg bg-indigo-600 p-2.5 font-semibold text-white disabled:opacity-50"
            >
              {submitting ? 'Registrando...' : 'Crear cuenta'}
            </button>
          )}
        </form.Subscribe>
      </form>

      <p className="mt-5 text-sm">
        <Link to="/login" className="text-indigo-700">
          Volver al inicio de sesión
        </Link>
      </p>
    </section>
  );
}