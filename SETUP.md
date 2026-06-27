# SETUP — strom für alle

## Voraussetzungen

- Docker Desktop (Mac/Windows) oder Docker Engine + Docker Compose (Linux/Raspi)
- Git

## Lokale Entwicklung (MacBook)

### 1. Repo klonen

```bash
git clone <repo-url>
cd stromfueralle
```

### 2. `.env` anlegen

```bash
cp .env.example .env
```

Dann `.env` öffnen und die Werte eintragen:

```env
POSTGRES_USER=stromfueralle
POSTGRES_PASSWORD=<beliebiges lokales Passwort>
POSTGRES_DB=stromfueralle

DATABASE_URL=postgresql://stromfueralle:<selbes Passwort>@db:5432/stromfueralle

# Langer zufälliger String — z.B. mit: openssl rand -hex 32
SECRET_KEY=<zufälliger langer String>

ADMIN_USERNAME=admin
# Das Passwort für den Admin-Login (lokal frei wählbar)
ADMIN_DEFAULT_PASSWORD=GreenData2026!
```

> **Wichtig:** `.env` wird nicht committed (steht in `.gitignore`). Nie echte Zugangsdaten in `.env.example` eintragen.

### 3. Starten

```bash
docker compose up --build -d
```

Der erste Start:
- Baut das Web-Image (dauert ~30s beim ersten Mal)
- Wartet bis PostgreSQL healthy ist
- Führt automatisch `alembic upgrade head` aus (erstellt die Tabellen)
- Legt den Admin-User aus `ADMIN_USERNAME` + `ADMIN_DEFAULT_PASSWORD` an (nur wenn noch keiner existiert)

### 4. App aufrufen

```
http://localhost:8000
```

Login mit den Werten aus `.env` (`ADMIN_USERNAME` / `ADMIN_DEFAULT_PASSWORD`).

### 5. Logs beobachten

```bash
docker compose logs -f web
```

### 6. Stoppen

```bash
docker compose down
```

Daten bleiben erhalten (PostgreSQL-Volume bleibt). Zum vollständigen Reset inkl. Daten:

```bash
docker compose down -v
```

---

## Deployment auf dem Raspberry Pi (Produktion)

### Erstmalig einrichten

```bash
# Auf dem Raspi (via SSH oder Raspberry Pi Connect):
git clone <repo-url> /opt/stromfueralle
cd /opt/stromfueralle
cp .env.example .env
nano .env   # Produktionswerte eintragen (starkes Passwort, echter SECRET_KEY)
docker compose up --build -d
```

### Update deployen

```bash
cd /opt/stromfueralle
git pull
docker compose up --build -d
```

Das reicht — `alembic upgrade head` läuft automatisch beim Container-Start, neue Migrations werden also automatisch angewendet.

### Produktions-.env Checkliste

- [ ] `POSTGRES_PASSWORD`: starkes, zufälliges Passwort
- [ ] `SECRET_KEY`: `openssl rand -hex 32` ausgeben und eintragen
- [ ] `ADMIN_DEFAULT_PASSWORD`: **nicht** `GreenData2026!` — eigenes sicheres Passwort wählen
- [ ] `.env` hat Dateirechte 600: `chmod 600 .env`

---

## Datenbankstruktur

| Tabelle | Inhalt |
|---------|--------|
| `users` | Admin-Login (username, password_hash) |
| `members` | Vereinsmitglieder (Mitgliedsnummer ab 1000) |
| `tariffs` | Tarif-Konfiguration (Bezug/Einspeisung ct/kWh, Mitgliedsbeitrag EUR/Jahr) |

## Alembic (Migrations)

Neue Migration anlegen (nach Model-Änderung):

```bash
docker compose run --rm web alembic revision --autogenerate -m "beschreibung"
```

Manuell auf aktuellem Stand bringen:

```bash
docker compose run --rm web alembic upgrade head
```
