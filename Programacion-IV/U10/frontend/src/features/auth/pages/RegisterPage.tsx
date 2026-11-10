import { useState } from 'react';
import { useForm } from '@tanstack/react-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function RegisterPage() {
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { register } = useAuth();
  const form = useForm({
    defaultValues: { nombre: '', apellido: '', email: '', celular: '', password: '' },
    onSubmit: async ({ value }) => {
      setError('');
      try {
        const datosRegistro = {
          nombre: value.nombre.trim(),
          apellido: value.apellido.trim(),
          email: value.email.trim(),
          celular: value.celular.trim() || null,
          password: value.password,
        };
        await register(datosRegistro);
        navigate('/login', { replace: true, state: { registered: true } });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'No se pudo registrar la cuenta.');
      }
    },
  });
  return (
    <section className="mx-auto my-10 max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
      <h1 className="text-2xl font-bold">Crear cuenta</h1>
      <p className="mt-2 mb-6 text-sm text-slate-600">
        Registrate para consultar el catálogo de FoodStore.
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
        <form.Field name="nombre">
          {(field) => (
            <label className="block text-sm font-medium">
              Nombre
              <input
                required
                maxLength={80}
                type="text"
                autoComplete="given-name"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(event) => field.handleChange(event.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-300 p-2.5"
              />
            </label>
          )}
        </form.Field>

        <form.Field name="apellido">
          {(field) => (
            <label className="block text-sm font-medium">
              Apellido
              <input
                required
                maxLength={80}
                type="text"
                autoComplete="family-name"
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
                maxLength={254}
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

        <form.Field name="celular">
          {(field) => (
            <label className="block text-sm font-medium">
              Celular (opcional)
              <input
                maxLength={20}
                type="tel"
                autoComplete="tel"
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
        <p className="text-xs text-slate-500">
          Contraseña: al menos 8 caracteres y hasta 72 bytes UTF-8.
        </p>
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


