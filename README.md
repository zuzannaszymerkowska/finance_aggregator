# Finance Aggregator (Portfolio Tracker)

Aplikacja webowa do śledzenia wartości portfela inwestycyjnego w różnych walutach z automatycznym przeliczaniem na PLN na podstawie kursów NBP.

## Demo
Link do aplikacji: [https://finance-aggregator.onrender.com](https://finance-aggregator.onrender.com)

## 🛠 Stos technologiczny
- **Framework:** Django 4.2
- **Język:** Python 3.11
- **Baza danych:** SQLite (Produkcja: Render Ephemeral)
- **API:** Narodowy Bank Polski (NBP API)
- **Konteneryzacja:** Docker & Docker Compose
- **CI/CD:** GitHub Actions & Render

## 🏗 Architektura i Funkcje
- **Relacyjna baza danych:** Modele User, Currency i Asset połąone kluczami obcymi.
- **Caching:** Kursy walut są przechowywane w pamięci podręcznej (Django Cache) przez 5 minut, aby ograniczyć liczbę zapytań do API NBP.
- **Bezpieczeństwo:** Pełna obsługa logowania i autoryzacji. Dane wrażliwe ukryte w zmiennych środowiskowych.
- **Automatyzacja:** Skrypt `build.sh` automatycznie tworzy superużytkownika i konfiguruje początkowe waluty.

## 🚦 CI/CD
- **CI (Continuous Integration):** Przy każdym wypchnięciu kodu na GitHub uruchamiane są testy jednostkowe (`portfolio/tests.py`).
- **CD (Continuous Deployment):** Po pomyślnym przejściu testów, aplikacja jest automatycznie wdrażana na platformę Render.

## 🐳 Uruchomienie lokalne (Docker)
1. Sklonuj repozytorium.
2. Skopiuj `.env.example` do `.env`.
3. Uruchom `docker-compose up --build`.
4. Aplikacja dostępna pod adresem `http://localhost:8000`.