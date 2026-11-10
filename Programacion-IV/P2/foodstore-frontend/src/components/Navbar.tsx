interface NavbarProps {
  cantidad: number
  onCrear: () => void
}

export function Navbar({ cantidad, onCrear }: NavbarProps) {
  return (
    <header className="bg-emerald-800 text-white shadow">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-5 py-5">
        <div>
          <h1 className="text-2xl font-bold">Food Store</h1>
          <p className="text-sm text-emerald-100">Administración de productos · {cantidad} registrados</p>
        </div>
        <button onClick={onCrear} className="rounded-lg bg-white px-4 py-2 font-semibold text-emerald-800 hover:bg-emerald-50">
          + Nuevo producto
        </button>
      </div>
    </header>
  )
}
