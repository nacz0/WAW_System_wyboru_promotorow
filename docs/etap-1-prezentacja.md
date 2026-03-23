---
marp: true
theme: default
paginate: true
---

# System Wyboru Promotorow
## Etap 1

Projekt systemu, architektura i stos technologiczny

**Zespolowy projekt aplikacji webowej**  
Technologie: **FastAPI + React + PostgreSQL**

---

# Cel projektu

Zaprojektowanie systemu webowego wspierajacego wybor promotorow przez studentow.

System ma:

- uporzadkowac proces zapisow,
- uwzgledniac limity miejsc u promotorow,
- respektowac ranking studentow wedlug sredniej,
- obslugiwac prace indywidualne i zespolowe,
- automatyzowac przydzial i raportowanie wynikow.

---

# Problem do rozwiazania

Proces wyboru promotora jest organizacyjnie trudny, bo trzeba jednoczesnie uwzglednic:

- kolejnosc studentow wynikajaca ze sredniej ocen,
- trzy preferencje promotora,
- ograniczona liczbe miejsc u promotorow,
- zespoly projektowe,
- termin zamkniecia wyborow,
- koniecznosc wygenerowania czytelnych wynikow.

Projektowany system ma te zasady egzekwowac automatycznie i deterministycznie.

---

# Uzytkownicy systemu

## Administrator

- zarzadza studentami i promotorami,
- ustala limity miejsc,
- definiuje harmonogram,
- tworzy zespoly,
- przeglada wyniki i generuje raporty.

## Student

- przeglada liste promotorow,
- potwierdza srednia,
- wybiera 3 preferencje,
- moze nalezec do zespolu,
- zmienia wybor do konca terminu.

## Promotor

- publikuje propozycje tematow,
- przeglada opis procesu,
- po zakonczeniu widzi przypisanych studentow lub zespoly.

---

# Najwazniejsze wymagania funkcjonalne

- logowanie i podzial na role,
- zarzadzanie lista studentow i promotorow,
- import studentow z CSV,
- obsluga zespolow projektowych,
- zapis 3 preferencji promotora,
- automatyczny przydzial po zakonczeniu naboru,
- raporty PDF i XLSX,
- blokada zmian po terminie,
- statystyki obciazenia promotorow.

---

# Wymagania niefunkcjonalne

- aplikacja webowa dostepna przez przegladarke,
- relacyjna baza danych,
- bezpieczne uwierzytelnianie i autoryzacja,
- integralnosc danych,
- obsluga wielu uzytkownikow jednoczesnie,
- deterministyczny algorytm przydzialu,
- responsywny interfejs,
- mozliwosc odtwarzania danych po awarii,
- zgodnosc z zasadami ochrony danych osobowych.

---

# Proponowana architektura

System zostal zaprojektowany w architekturze **3-warstwowej**:

1. **Frontend**  
   React odpowiada za interfejs uzytkownika.

2. **Backend API**  
   FastAPI realizuje logike biznesowa i udostepnia endpointy.

3. **Baza danych**  
   PostgreSQL przechowuje dane i pilnuje integralnosci.

---

# Diagram architektury

```text
Przegladarka
     |
     v
Frontend (React)
     |
     v
Backend API (FastAPI)
     |
     v
PostgreSQL

Dodatkowe moduly backendu:
- algorytm przydzialu
- raporty PDF/XLSX
- powiadomienia e-mail
```

---

# Dlaczego taki stos technologiczny

## React

- wygodny do budowy paneli i formularzy,
- dobry pod podzial na role,
- sprawdzony ekosystem.

## FastAPI

- szybkie tworzenie REST API,
- walidacja danych przez Pydantic,
- automatyczna dokumentacja API,
- czytelna struktura projektu.

## PostgreSQL

- silna integralnosc danych,
- dobre wsparcie dla relacji i ograniczen,
- stabilnosc i dojrzalosc.

---

# Moduly systemu

- uwierzytelnianie i autoryzacja,
- zarzadzanie studentami i promotorami,
- zarzadzanie zespolami,
- harmonogram wyborow,
- zapis preferencji,
- algorytm przydzialu,
- raportowanie,
- statystyki i podglad wynikow.

---

# Kluczowa logika biznesowa

Po zamknieciu wyborow system:

1. sortuje studentow lub zespoly wedlug sredniej,
2. dla kazdego rekordu sprawdza preferencje 1, 2, 3,
3. przypisuje pierwszego promotora z wolnym limitem,
4. zapisuje wynik w sposob powtarzalny.

### Dla zespolow

- wyboru dokonuje lider,
- liderem jest student z najwyzsza srednia,
- jeden promotor jest przypisywany do calego zespolu.

---

# Wstepny model danych

Glowne encje:

- `User`
- `Student`
- `Supervisor`
- `Team`
- `TeamMember`
- `SelectionRound`
- `Preference`
- `Assignment`
- `TopicProposal`

Model relacyjny pozwala rozdzielic:

- konta i role,
- dane studentow,
- zespoly,
- preferencje,
- finalne wyniki przydzialu.

---

# Przykladowe relacje

```text
User 1..1 -> Student
User 1..1 -> Supervisor
Team 1..* -> TeamMember
Student *..1 -> Team
Supervisor 1..* -> TopicProposal
SelectionRound 1..* -> Preference
Supervisor 1..* -> Assignment
Student/Team 1..1 -> Assignment
```

---

# Bezpieczenstwo i spojnosc danych

System powinien zapewnic:

- hashowanie hasel,
- autoryzacje oparta o role,
- walidacje danych po stronie backendu,
- klucze obce i ograniczenia unikalnosci,
- transakcyjne wykonanie przydzialu,
- blokade zmian po terminie.

---

# Podzial realizacji na etapy kursu

## Etap 1

- projekt systemu,
- architektura,
- opis stosu technologicznego,
- dokumentacja.

## Etap 2

- dzialajacy backend,
- endpointy API,
- projekt widokow aplikacji klienckiej.

## Etap 3

- pelny dzialajacy system,
- algorytm przydzialu,
- raporty,
- kompletna dokumentacja projektu.

---

# Rezultat etapu 1

Na obecnym etapie przygotowano:

- koncepcje systemu,
- podzial na role i moduly,
- architekture rozwiazania,
- opis stosu technologicznego,
- wstepny model danych,
- plan dalszej implementacji.

To stanowi baze do realizacji backendu i frontendu w kolejnych etapach.

---

# Podsumowanie

Projekt odpowiada na rzeczywisty problem organizacyjny wydzialu.

Wybrana architektura:

- jest czytelna,
- wspiera dalszy rozwoj,
- pozwala zachowac spojne dane,
- dobrze pasuje do wymagan kursowych.

**FastAPI + React + PostgreSQL** to zestaw odpowiedni do budowy tego systemu.
