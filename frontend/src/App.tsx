import { Routes, Route } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Home } from "./pages/Home";
import { Login } from "./pages/Login";
import { Promotorzy } from "./pages/Promotorzy";
import { MojeWybory } from "./pages/MojeWybory";
import { ProfilPromotora } from "./pages/ProfilPromotora";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/promotorzy" element={<Promotorzy />} />
        <Route path="/profil/:id" element={<ProfilPromotora />} />
        <Route path="/moje-wybory" element={<MojeWybory />} />
        {/* Placeholder routes for future development */}
        <Route path="/rejestracja" element={<div className="py-20 text-center font-bold text-2xl">Rejestracja - Etap 2</div>} />
      </Routes>
    </Layout>
  );
}
