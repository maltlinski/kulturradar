# Kulturradar Bologna

Geprüfte Tanz-, Opern- und Theatertermine in Bologna und der Emilia-Romagna, dazu Highlights in Florenz, Mailand, Turin und Venedig. Eine statische Webseite mit Agenda, Wochen- und Monatsansicht, Filtern, Top-Tipps, Fristen und abonnierbaren Kalender-Feeds.

## So funktioniert es

```
             täglich (GitHub Actions)                         wöchentlich (Claude)
┌────────────────────────────────────────────┐   ┌──────────────────────────────────────────┐
│ prune.py     Vergangenes löschen           │   │ prüft nächste 14 Tage + alle 🟡 an der    │
│ watch.py     bekannte Quellen prüfen  ─────┼──▶│ Quelle, verifiziert Kandidaten, sucht     │
│ discover.py  Kalenderseiten absuchen ─────┼──▶│ Neues, schreibt Wochenbrief               │
│ build.py     Seite + .ics neu bauen        │   │ → Pull Request                            │
└───────────────┬────────────────────────────┘   └──────────────────┬───────────────────────┘
                │ Auffälligkeiten → Issue                            │ Malte merged
                ▼                                                    ▼
                      GitHub Pages: Seite + kulturradar.ics / tanz.ics / ausfluege.ics / fristen.ics
```

- **Daten** liegen in `data/events.json`, `data/deadlines.json`, `data/meta.json`. Jede Änderung ist ein Commit und damit nachvollziehbar.
- **Der tägliche Lauf** ändert nur Deterministisches (vergangene Termine löschen) und meldet Auffälligkeiten (Absage, Ausverkauf, Datum verschwunden, Quelle nicht erreichbar) als Issue. Neue Funde landen ungeprüft in `data/candidates.json`.
- **Der Wochenlauf** (Claude) prüft nach den Regeln in `CLAUDE.md` und schlägt Änderungen als Pull Request vor. Veröffentlicht wird erst nach dem Merge.

## Kalender abonnieren

Nach der Veröffentlichung unter <https://maltlinski.github.io/kulturradar/>:

| Feed | Inhalt |
|---|---|
| `kulturradar.ics` | Alle Termine in Bologna und der Region |
| `tanz.ics` | Tanz, Ballett, Workshops, offene Proben (inkl. Ausflüge) |
| `ausfluege.ics` | Florenz, Mailand, Turin, Venedig |
| `fristen.ics` | Fristen und Anmeldungen als ganztägige Termine |

Google Kalender: „Weitere Kalender“ → „Per URL“. Apple Kalender: „Ablage“ → „Neues Kalenderabonnement“ (am iPhone: Einstellungen → Kalender → Accounts → Abonnierter Kalender). Abonnieren, nicht importieren, dann aktualisiert sich der Kalender von selbst.

## Lokal arbeiten

```
pip install -r requirements.txt
python -m pytest -q tests
python scripts/validate.py
python scripts/build.py && python -m http.server -d _site 8000
```

## Einrichtung

Siehe `prompts/cloud-session/00-START-HIER.md`.

## Herkunft der Daten

Startbestand: „Kulturradar Master“ in Notion, Version 9 (Prüfung vom 19.10.2026), mit allen Status und Belegen übernommen. Ein Eintrag (Wagner, *Der fliegende Holländer*, Piacenza) wurde dabei von ✅ auf 🟡 gesetzt, weil seine einzige Quelle (teatripiacenza.it) keine Tier-1/2-Quelle ist.
