# CLAUDE.md — Projektkontext für Claude Code

Diese Datei wird bei jedem Start von Claude Code automatisch gelesen. Sie ist die Single Source of Truth für Tech-Entscheidungen, Scope und Konventionen in diesem Repo. **Nicht widersprechen, nicht neu diskutieren — nur umsetzen.**

## Projekt

**„strom für alle"** — Verwaltungsplattform für die Energiegemeinschaft **EEG Strompool Feldkirchen Süd-West** (ZVR 1778816746). Diplomarbeitsprojekt von Fabian (HTL Kärnten), Projektleiter Patrick Ropper (Obmann des Vereins). Domain (final): `stromfueralle.at`. Übergangsweise erreichbar unter `webapp.mechtronix.at`.

Harte Deadline für den MVP: **1. Juli 2026**. Danach folgen Multi-Tenancy, ESP32-Integration, Live-Dashboard, Abrechnung, EDA-Import — das alles ist für diesen Sprint **out of scope**, auch wenn es naheliegt, es "gleich mitzubauen". Bitte aktiv widerstehen.

## Tech-Stack (festgelegt — nicht zur Diskussion)

- Python 3.12 + FastAPI
- Jinja2 (Server-Side-Rendering, kein SPA-Framework)
- PostgreSQL 16
- Bootstrap 5 (CDN oder vendored, kein Build-Step nötig)
- LaTeX via `subprocess` (PDF-Generierung für Vereinbarungen)
- Docker Compose für lokale Entwicklung und Deployment auf dem Raspi

**Single-EEG hartcodiert.** Keine Mandantenfähigkeit, keine Tenant-ID-Spalten, kein "was wäre wenn ein zweiter Verein das nutzt" — das kommt explizit erst nach dem 1. Juli. Wenn eine Implementierung sich nur durch Multi-Tenancy "sauberer" anfühlt, trotzdem die einfache Single-Tenant-Variante bauen.

## MVP-Scope (bis 1. Juli)

1. Admin-Login (einfache Session-Auth, kein OAuth, kein 2FA)
2. Mitglieder-CRUD (Mitgliedsnummer beginnt bei **1000**, fortlaufend)
3. Tarif-Konfiguration (Bezug/Einspeisung in ct/kWh, Mitgliedsbeitrag in EUR/Jahr — administrierbar, nicht hartcodiert in Templates)
4. Bezugsvereinbarung + Einspeisevereinbarung als LaTeX-generiertes PDF (pro Mitglied)
5. E-Mail-Versand über Office 365 SMTP (Code fertig, Aktivierung/Konfiguration kann nach dem 1. Juli erfolgen — Feature-Flag oder einfach ENV-Var-gesteuert)
6. „strom für alle"-Branding (Bootstrap-Theme, Logo-Platzhalter wo nötig)
7. `/live`-Route als Platzhalter (zeigt vorerst nur ein Bagger-Bild/Platzhalter-Text — "Live-Dashboard kommt bald")

**Nicht in diesem Sprint:** Multi-Tenancy, ESP32, echtes Live-Dashboard, Abrechnungslogik, EDA-Import.

## Vereinsdaten (für Templates, Verträge, Footer etc.)

```
Name:            EEG Strompool Feldkirchen Süd-West
ZVR:             1778816746
Marktpartner-ID: RC108175
Netzbetreiber:   KNG-Kärnten Netz GmbH
Obmann:          Patrick Ropper
Steuermodell:    Kleinunternehmer gemäß § 6 Abs 1 Z 27 UStG (kein USt-Ausweis auf Dokumenten/Rechnungen)
```

## Tarife (administrierbar, Default-Werte)

```
Bezug (Mitglied von Gemeinschaft):    12 ct/kWh
Einspeisung (Mitglied an Gemeinschaft): 8 ct/kWh
Mitgliedsbeitrag:                      24 EUR/Jahr
```

Diese Werte müssen über die Tarif-Config-Seite änderbar sein, nicht hartcodiert in LaTeX-Templates oder Python.

## LaTeX-Templates

Referenz-Templates liegen in `latex_templates/`:
- `bezugsvereinbarung.tex`
- `einspeisevereinbarung.tex`

Diese stammen aus Patricks Repo (`ropperp/eeg-platform/latex-service/templates/`) und sind von ihm **als Logik-Referenz freigegeben** — d.h. die fachliche/rechtliche Struktur (welche Felder, welche Paragraphen, welche Formulierungen) übernehmen, aber an unseren Stack (FastAPI + subprocess statt seinem latex-service) und unser Branding anpassen. Bei Unklarheiten in der Vorlage: lieber nachfragen (an Fabian) als raten, da es sich um rechtsverbindliche Vereinbarungstexte handelt.

PDF-Generierung läuft über `subprocess` (z.B. `pdflatex` oder `lualatex` im Docker-Container). Templates werden mit Jinja2 (oder einem Jinja2-kompatiblen LaTeX-Escaping-Ansatz) befüllt, dann kompiliert.

## Auth & Sicherheit

- Standardpasswort `GreenData2026!` wird **ausschließlich** als Default in `.env` (lokal, nicht committed) verwendet, nie hartcodiert im Code.
- `.env.example` mit Platzhaltern gehört ins Repo, `.env` selbst in `.gitignore`.
- Passwort-Hashing für den Admin-User (z.B. passlib/bcrypt) — auch im MVP, auch wenn es "nur" ein Verein ist. Kein Klartext-Passwort in der DB.
- Repo ist **public** — niemals echte Zugangsdaten, SMTP-Passwörter oder ähnliches committen. Alles Sensible über `.env`.

## Deployment

- Lokale Entwicklung: Docker Compose (Postgres + Webapp-Container) auf Fabians MacBook
- Produktion: Patricks Raspberry Pi, erreichbar via Raspberry Pi Connect, Pfad `/opt/stromfueralle/`
- Deployment-Workflow: `git pull` + `docker compose up -d --build` (oder vergleichbar — in SETUP.md dokumentieren)
- Übergangs-URL: `webapp.mechtronix.at`, später `stromfueralle.at`

## Projektbegleitende Dokumentation

Drei Dateien im Repo-Root immer aktuell halten:

- **CLAUDE.md** (diese Datei) — Kontext für Claude Code, nur bei echten Scope-/Stack-Änderungen anfassen
- **PROJEKTSTAND.md** — laufendes Tagebuch: was ist fertig, was ist offen, bekannte Probleme, nächste Schritte. Nach jeder Arbeitssession aktualisieren.
- **SETUP.md** — Schritt-für-Schritt-Anleitung zum lokalen Aufsetzen (Docker Compose, ENV-Variablen, Seed-Daten) und zum Deployment auf dem Raspi. Muss so klar sein, dass auch Patrick (nicht der Hauptentwickler) damit deployen kann.

## Arbeitsweise / Konventionen

- Fabian hat begrenzte Coding-Erfahrung. Bei jeder nicht-trivialen Änderung kurz erklären: (1) was die Datei/Funktion tut, (2) warum die Änderung so gemacht wird, (3) wie der Diff zu lesen ist.
- Commits klein und beschreibend halten (kein "fix stuff").
- Deutsche Kommentare/Doku sind ok wo es um fachliche/rechtliche Inhalte geht (Vereinsrecht, Energiegemeinschaft-Begriffe); Code selbst (Variablen, Funktionsnamen) auf Englisch, wie überall im Projekt üblich.
- Vor jeder größeren Änderung kurz den Plan skizzieren, bevor Code geschrieben wird — kein stilles Drauflosimplementieren bei mehrschrittigen Aufgaben.
- Bei Unsicherheit über rechtliche/fachliche Details der Vereinbarungen (Steuerrecht, Energiegemeinschaftsrecht): nachfragen statt annehmen.

## Nicht tun

- Keine Multi-Tenancy-Vorbereitung "für später"
- Keine Cloud-Services einführen, die nicht im Stack stehen (kein Firebase, kein Auth0, kein managed Postgres)
- Kein Frontend-Framework (React/Vue) einführen — Jinja2 + Bootstrap reicht für den MVP
- Keine echten Zugangsdaten oder Secrets committen
