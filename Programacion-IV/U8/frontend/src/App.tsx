import { Routes, Route, Navigate } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { CategoriasPage } from "./pages/CategoriasPage";
import { ProductsPage } from "./pages/ProductsPage";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />
      <div className="flex-1">
        <Routes>
          <Route path="/" element={<Navigate to="/categorias" replace />} />
          <Route path="/categorias" element={<CategoriasPage />} />
          <Route path="/productos" element={<ProductsPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;