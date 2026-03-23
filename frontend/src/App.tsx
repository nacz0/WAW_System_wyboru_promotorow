const modules = [
  "Logowanie i role",
  "Studenci i promotorzy",
  "Zespoly projektowe",
  "Preferencje wyboru",
  "Automatyczny przydzial",
  "Raporty PDF i XLSX",
];

const architecture = [
  { layer: "Frontend", tech: "React + TypeScript", description: "Panele dla administratora, studenta i promotora." },
  { layer: "Backend", tech: "FastAPI", description: "API REST, logika biznesowa i walidacja." },
  { layer: "Baza danych", tech: "PostgreSQL", description: "Relacyjny model danych i integralnosc." },
];

export default function App() {
  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Etap 1</p>
        <h1>System Wyboru Promotorow</h1>
        <p className="lead">
          Projekt architektury aplikacji webowej wspierajacej przydzial promotorow
          dla prac indywidualnych i zespolowych.
        </p>
      </section>

      <section className="grid">
        <article className="card">
          <h2>Stos technologiczny</h2>
          <ul>
            {architecture.map((item) => (
              <li key={item.layer}>
                <strong>{item.layer}:</strong> {item.tech} - {item.description}
              </li>
            ))}
          </ul>
        </article>

        <article className="card">
          <h2>Zakres systemu</h2>
          <ul>
            {modules.map((module) => (
              <li key={module}>{module}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="card">
        <h2>Zasady biznesowe</h2>
        <p>
          Przydzial promotorow bedzie realizowany po zamknieciu naboru na podstawie
          sredniej ocen, kolejnosci preferencji i limitow miejsc u promotorow.
          Dla zespolow decyzje podejmuje lider wyznaczany automatycznie jako student
          z najwyzsza srednia.
        </p>
      </section>
    </main>
  );
}
