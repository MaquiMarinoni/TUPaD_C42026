    interface NavbarProps {
    titulo?: string;
    }

    export const Navbar = ({ titulo = "Food Store - Gestión de Categorías" }: NavbarProps) => {
    return (
        <header className="bg-slate-900 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">

            <h1 className="text-xl font-bold tracking-tight text-white sm:text-2xl">
                {titulo}
            </h1>
            </div>
        </div>
        </header>
    );
    };