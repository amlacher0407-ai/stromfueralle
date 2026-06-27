# PROJEKTSTAND — strom für alle

## Tag 1 — 2026-06-27

### Fertig

- **Docker-Infrastruktur**: `docker-compose.yml` mit postgres:16 (Healthcheck), Web-Container (Python 3.12-slim), Volume-Persistenz
- **FastAPI-Skeleton**: App-Factory (`create_app()`), Jinja2-Templates, Bootstrap 5 via CDN, Navbar mit Login-Status, Footer mit Vereinsdaten
- **Routen**: `/` (Startseite), `/live` (Platzhalter), `/login`, `/logout`, `/members` (CRUD)
- **DB-Schema**: SQLAlchemy 2.0-Style, Tabellen `users`, `members`, `tariffs`; Alembic-Migration via `--autogenerate` generiert
- **Auth**: Session-basiert (Starlette SessionMiddleware), Passwort-Hashing mit bcrypt, Admin-User wird beim ersten Start aus ENV angelegt
- **Mitglieder-CRUD**: Liste, Anlegen (Mitgliedsnummer ab 1000, automatisch), Bearbeiten, Löschen mit Bestätigungsdialog
- **Smoke-Tests**: Login, Mitglied anlegen (Nummer 1000), /members nur mit Session erreichbar ✓

### Bekannte Einschränkungen

- `bcrypt` auf 3.2.2 gepinnt wegen passlib 1.7.4 Inkompatibilität mit bcrypt >= 4.0
- Kein `--reload` im Docker-Container: nach Code-Änderungen `docker compose up --build -d web` nötig
- `updated_at` in `members` wird nur auf DB-Ebene via `server_default` gesetzt; `onupdate=func.now()` benötigt in Alembic ggf. eine separate Migration wenn aktiv genutzt

### Offen für Tag 2

- Tarif-Konfigurationsseite (`/tariffs` — Bezug/Einspeisung/Mitgliedsbeitrag änderbar)
- LaTeX-PDF-Generierung (Bezugsvereinbarung + Einspeisevereinbarung pro Mitglied)
- E-Mail-Versand via Office 365 SMTP (Feature-Flag via ENV)
- Download-Button für PDFs auf der Mitglieder-Detailseite
