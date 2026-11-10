import { Link } from 'react-router-dom';
export function UnauthorizedPage() {
  return (
    <section className="mx-auto max-w-xl p-10">
      <h1 className="text-2xl font-bold">Acceso denegado</h1>
      <p className="my-4">Tu usuario no tiene permisos para ingresar a esta sección.</p>
      <Link to="/categories" className="text-indigo-700">
        Volver al catálogo
      </Link>
    </section>
  );
}

