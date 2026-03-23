# System Wyboru Promotorow

Projekt dotyczy budowy aplikacji webowej wspierajacej proces wyboru promotorow przez studentow z uwzglednieniem limitow miejsc, rankingu opartego o srednia ocen, preferencji studentow oraz zespolow projektowych.

Repozytorium w obecnej postaci zawiera materialy dla etapu 1:

- opis problemu i zakresu projektu,
- architekture systemu,
- opis stosu technologicznego,
- wstepny model danych,
- plan implementacji kolejnych etapow,
- minimalny szkielet aplikacji w technologiach FastAPI, React i PostgreSQL.

## Stos technologiczny

- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic
- Frontend: React, TypeScript, Vite
- Baza danych: PostgreSQL
- Infrastruktura lokalna: Docker Compose
- Uwierzytelnianie: JWT
- Raportowanie: PDF i XLSX w kolejnych etapach

## Struktura repozytorium

```text
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
frontend/
  src/
docs/
  etap-1.md
docker-compose.yml
.env.example
```

## Dokumentacja etapu 1

Glowny dokument dla pierwszego etapu znajduje sie tutaj:

- [docs/etap-1.md](c:\Users\natma\Documents\GitHub\WAW_System_wyboru_promotorow\docs\etap-1.md)

## Uruchomienie lokalne

Na tym etapie jest to szkielet startowy projektu.

1. Skopiuj `.env.example` do `.env`.
2. Uruchom uslugi przez `docker compose up --build`.
3. Backend bedzie dostepny pod `http://localhost:8000`.
4. Frontend bedzie dostepny pod `http://localhost:5173`.

## Zakres etapu 1

Etap 1 koncentruje sie na zaprojektowaniu rozwiazania, a nie na pelnej implementacji procesow biznesowych. Przygotowane artefakty stanowia baze do dalszych etapow, w tym implementacji logowania, wyboru promotorow, algorytmu przydzialu, raportowania i powiadomien e-mail.
