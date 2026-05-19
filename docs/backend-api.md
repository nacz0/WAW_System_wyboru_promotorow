# Backend API - etap 2

Backend udostepnia REST API w FastAPI pod prefiksem `/api`. Dokumentacja interaktywna po uruchomieniu aplikacji jest dostepna pod:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Zakres implementacji

Zaimplementowane moduly:

- health check i opis projektu,
- logowanie JWT i endpoint aktualnego uzytkownika,
- uzytkownicy z rolami `admin`, `student`, `supervisor`,
- studenci i promotorzy,
- propozycje tematow promotorow,
- zespoly z automatycznym wyznaczaniem lidera wedlug najwyzszej sredniej,
- rundy wyboru promotorow,
- preferencje studentow albo zespolow,
- deterministyczny przydzial promotorow na podstawie sredniej, preferencji i limitow miejsc.
- eksport wynikow przydzialu do CSV.
- testy jednostkowe algorytmu przydzialu.

## Glowne endpointy

| Metoda | Sciezka | Opis |
| --- | --- | --- |
| `GET` | `/api/health` | Sprawdzenie stanu API |
| `GET` | `/api/overview` | Opis modulow projektu |
| `POST` | `/api/auth/login` | Logowanie i pobranie tokenu JWT |
| `GET` | `/api/auth/me` | Dane aktualnego uzytkownika na podstawie tokenu Bearer |
| `POST` | `/api/users` | Utworzenie uzytkownika |
| `GET` | `/api/users` | Lista uzytkownikow |
| `POST` | `/api/students` | Utworzenie profilu studenta dla uzytkownika z rola `student` |
| `GET` | `/api/students` | Lista studentow |
| `POST` | `/api/supervisors` | Utworzenie profilu promotora dla uzytkownika z rola `supervisor` |
| `PATCH` | `/api/supervisors/{id}` | Zmiana limitu miejsc lub opisu promotora |
| `POST` | `/api/supervisors/{id}/topics` | Dodanie propozycji tematu |
| `POST` | `/api/teams` | Utworzenie zespolu |
| `POST` | `/api/teams/{id}/members` | Dodanie studenta do zespolu |
| `POST` | `/api/rounds` | Utworzenie rundy wyboru |
| `PATCH` | `/api/rounds/{id}/status` | Zmiana statusu rundy |
| `POST` | `/api/preferences` | Dodanie preferencji 1-3 dla studenta albo zespolu |
| `GET` | `/api/preferences?selection_round_id={id}` | Lista preferencji rundy |
| `POST` | `/api/assignments/run/{selection_round_id}` | Uruchomienie algorytmu przydzialu |
| `GET` | `/api/assignments?selection_round_id={id}` | Lista wynikow przydzialu |
| `POST` | `/api/demo/seed` | Utworzenie danych demonstracyjnych i uruchomienie przydzialu |
| `GET` | `/api/reports/assignments.csv?selection_round_id={id}` | Eksport wynikow przydzialu do CSV zgodnego z Excelem |

## Reguly walidacji

- Student musi wskazywac istniejacego uzytkownika z rola `student`.
- Promotor musi wskazywac istniejacego uzytkownika z rola `supervisor`.
- Srednia studenta musi byc w zakresie `2.0-5.0`.
- Preferencja ma priorytet `1`, `2` albo `3`.
- Preferencja nalezy dokladnie do jednego wlasciciela: studenta albo zespolu.
- Ten sam aktor nie moze wybrac tego samego promotora dwa razy w jednej rundzie.
- Ten sam aktor nie moze uzyc dwa razy tego samego priorytetu w jednej rundzie.
- Po zamknieciu lub przydzieleniu rundy API blokuje dodawanie preferencji.
- Student moze nalezec tylko do jednego zespolu.

## Autoryzacja

Backend obsluguje logowanie JWT przez `POST /api/auth/login`. Token nalezy podac w Swaggerze przez przycisk `Authorize` jako token Bearer.

Konta demonstracyjne po `POST /api/demo/seed` maja haslo `demo1234`:

- `admin@waw.edu.pl` - rola `admin`,
- `anna.zielinska@student.waw.edu.pl` - rola `student`,
- `jan.kowalski@waw.edu.pl` - rola `supervisor`.

Najwazniejsze reguly dostepu:

- `admin` tworzy i edytuje uzytkownikow, studentow, promotorow, zespoly oraz rundy,
- zalogowani uzytkownicy moga przegladac listy studentow, promotorow, zespolow, rund i wynikow,
- student moze pobrac swoje dane i zlozyc swoje preferencje,
- preferencje zespolu moze zlozyc tylko lider zespolu,
- promotor moze dodawac tematy tylko do swojego profilu,
- uruchomienie algorytmu przydzialu wymaga roli `admin`,
- eksport CSV wymaga roli `admin`,
- `POST /api/demo/seed` pozostaje otwarty, aby szybko przygotowac dane do prezentacji.

## Algorytm przydzialu

Endpoint `POST /api/assignments/run/{selection_round_id}`:

1. Usuwa poprzednie wyniki dla danej rundy, aby prezentacja byla powtarzalna.
2. Grupuje preferencje wedlug studenta albo zespolu.
3. Dla zespolu wybiera lidera z najwyzsza srednia; remisy rozstrzyga numer albumu.
4. Sortuje kandydatow malejaco po sredniej, a remisy stabilnie po numerze albumu albo nazwie zespolu.
5. Sprawdza preferencje w kolejnosci `1 -> 2 -> 3`.
6. Przydziela do pierwszego promotora z wystarczajaca liczba miejsc.
7. Dla zespolu zuzywa tyle miejsc, ilu studentow jest w zespole.
8. Zwraca liste przydzielonych oraz liste nieprzydzielonych z powodem.

## Testy

Testy algorytmu znajduja sie w `backend/tests/test_assignment.py`. Obejmują:

- pierwszenstwo studenta z wyzsza srednia,
- brak miejsc u promotora,
- przydzial zespolu z uwzglednieniem liczby czlonkow,
- automatyczne wskazanie lidera zespolu,
- powtarzalnosc wyniku bez duplikowania przydzialow.

Uruchomienie:

```powershell
python -m pytest backend/tests
```

## Przykladowy przebieg demonstracyjny

Najszybsza prezentacja:

1. Uruchom `POST /api/demo/seed`.
2. Zaloguj sie przez `POST /api/auth/login`, na przyklad jako `admin@waw.edu.pl` albo `anna.zielinska@student.waw.edu.pl` z haslem `demo1234`.
3. Uzyj tokenu w przycisku `Authorize` w Swaggerze.
4. Sprawdz `GET /api/auth/me`.
5. Otworz `GET /api/students`, `GET /api/supervisors`, `GET /api/preferences` i `GET /api/assignments`.
6. Pobierz raport przez `GET /api/reports/assignments.csv`.

Reczny przebieg:

1. Utworz uzytkownikow promotorow i studentow przez `/api/users`.
2. Dla studentow utworz profile przez `/api/students`.
3. Dla promotorow utworz profile przez `/api/supervisors`.
4. Opcjonalnie dodaj tematy przez `/api/supervisors/{id}/topics`.
5. Utworz runde przez `/api/rounds`.
6. Dodaj preferencje przez `/api/preferences`.
7. Uruchom przydzial przez `/api/assignments/run/{selection_round_id}`.
8. Sprawdz wynik przez `/api/assignments`.
