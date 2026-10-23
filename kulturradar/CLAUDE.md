# Kulturradar Bologna – Projektregeln für Claude

Dieses Repository ist Maltes geprüfter Kulturkalender für Bologna, die Emilia-Romagna und ausgewählte Ausflüge nach Florenz, Mailand, Turin und Venedig. Antworte und schreibe auf **Deutsch**. Nutzertexte (Seite, Wochenbrief, PR-Texte) sind kurz, sachlich, ohne Werbesprache.

## Für wen

Malte ist professioneller Tänzer (zeitgenössisch, Ballett, Ballroom) und Master-Student Kulturmanagement, im Erasmus-Semester in Bologna bis Februar 2027. Er will auf einen Blick sehen, was sich lohnt, was gratis oder ermäßigt ist und welche Fristen laufen.

Priorität bei Auswahl und Darstellung:
1. Zeitgenössischer Tanz und Ballett, Workshops, Masterclasses, Calls und Auditions für Profis
2. Oper und Musiktheater
3. Festivals, offene Proben, Hausführungen
4. Theater und Performance
5. Ballroom, Swing, Tango

## Aufbau

| Pfad | Inhalt |
|---|---|
| `data/events.json` | Alle Termine (Quelle der Wahrheit). Format: `schema/data.schema.json` |
| `data/deadlines.json` | Fristen und Anmeldungen |
| `data/meta.json` | Version, Prüfdaten, Top-Tipps, Link zum aktuellen Wochenbrief |
| `data/candidates.json` | Ungeprüfte Funde des täglichen Scrapers (nie direkt veröffentlichen) |
| `data/sources.yaml` | Quellen-Tiers, Kalenderseiten für den Scraper, Signalwörter |
| `site/index.html` | Die Webseite (statisch, liest `data/*.json`) |
| `scripts/` | `prune.py` (Vergangenes löschen), `validate.py` (Schema + Regeln), `build.py` (Seite + `.ics`-Feeds nach `_site/`) |
| `scraper/` | `watch.py` (bekannte Quellen täglich prüfen), `discover.py` (Kalenderseiten nach Neuem absuchen), `adapters/` |
| `briefs/` | Wochenbriefe `JJJJ-MM-TT.md` |
| `reports/` | Berichte des täglichen Laufs |
| `prompts/` | Prompts für den Wochenlauf und für die Einrichtung |

Befehle: `pip install -r requirements.txt` · `python -m pytest -q tests` · `python scripts/validate.py` · `python scripts/build.py` · `python scraper/watch.py --days 21` · `python scraper/discover.py`. Mit `KR_TODAY=JJJJ-MM-TT` lässt sich das Laufdatum für Tests festlegen.

Vor jedem Commit an `data/`: `python scripts/validate.py` muss ohne Fehler laufen.

## Datenmodell (Kurzfassung)

Ein Termin hat u. a.: `id` (stabiler Slug aus Titel und erstem Datum; **bestehende IDs nie ändern**, die Merkliste im Browser hängt daran), `title` (nur Werktitel), `artist`, `text` (vollständige Beschreibung in Markdown mit Links), `when` (Datumsangabe als Text), `dates` (Einzeltermine `{date, time}`; `time` als `"HH:MM"`, `"HH:MM + HH:MM"` oder `null`), `range` (nur für Zeitspannen über 7 Tage, z. B. Festivals), `venue`, `city`, `sparte`, `cat` (dance, ballet, workshop, probe, opera, theatre, music, social, tour, festival, art, other), `region` (bologna, er, trip), `status` (ok = ✅, check = 🟡, partial = ✅ mit 🟡-Anteil, cancel = ❌), `statusNote` (Begründung), `cancelledAt` (bei ❌, Datum der Feststellung), `free`, `discount`, `premiere`, `soldOut` (full, few, null), `sources` (Belege zuerst), `lastChecked`.

## Verifikationsregeln (strikt, nicht verhandelbar)

- Jeder Eintrag braucht einen Link auf eine Tier-1- oder Tier-2-Seite, bei Ausflügen auf eine der Trip-Quellen in `data/sources.yaml`. Tier 3 ist nur Discovery, nie Beleg.
- ✅ (`ok`) nur, wenn Datum, Ort und Titel auf dieser Seite selbst gesehen wurden. Sonst 🟡 (`check`) mit Grund in `statusNote`: „nur Presse“, „Widerspruch: A sagt X, B sagt Y“, „Seite nicht erreichbar am TT.MM.“.
- Nichts erfinden oder erschließen: keine Termine aus Mustern, keine Uhrzeiten, Preise oder Namen ohne Beleg.
- Jahreszahl jeder Quelle prüfen. Vorjahresseiten gelten nicht.
- Festival-Übersichten zeigen oft Zeitspannen inklusive Proben. Einzeltermine immer auf der Stückseite prüfen.
- Widerspruch Presse vs. Primärquelle: Primärquelle gilt. Zwei widersprüchliche Primärquellen: 🟡 und beide nennen.
- Seite nicht erreichbar: Status unverändert lassen, Vermerk „Quelle am TT.MM. nicht erreichbar“.
- Abgesagt oder verschoben: `status: cancel`, `cancelledAt` setzen, Hinweis in `statusNote`. `prune.py` löscht nach 7 Tagen.
- Top-Tipps nur aus ✅-Einträgen.
- Die Signalwörter aus `scraper/watch.py` sind nur Hinweise. Status erst ändern, wenn die Seite selbst es für genau diesen Termin sagt.
- Nichts kaufen, Malte nirgends anmelden, niemandem schreiben. Fristen nur melden.
- `robots.txt` und Nutzungsbedingungen der Seiten respektieren; Abrufe langsam und selten halten (siehe `scraper/fetch.py`).

## Quellen

Siehe `data/sources.yaml` (Tier 1, Tier 2, Tier 3, Trip-Quellen). Ausflüge: hohe Messlatte, nur Highlights, die eine Zugfahrt lohnen (international relevante Kompanien und Choreograf:innen, große Ballettproduktionen, Uraufführungen/italienische Erstaufführungen, bedeutende Opernpremieren mit starker Besetzung, besondere Festivals, Profi-Workshops/Calls/Auditions). Kein Routine-Theater, keine Tribute-Shows, keine Musicals. Höchstens etwa 20 Ausflugs-Einträge. Ausverkauf und Under-30/35-Angebote immer vermerken.

## Arbeitsweise

- Änderungen an `data/` aus Recherche-Läufen immer als Pull Request, mit Änderungsliste „alter Wert → neuer Wert, Quelle“ im PR-Text. Der tägliche Lauf darf `prune.py`-Ergebnisse, Berichte und `candidates.json` direkt auf `main` committen.
- Die Seite (`site/index.html`) ist ein eigenständiges HTML ohne Build-Schritt. Farben nur über die CSS-Variablen in `:root`, helles und dunkles Thema pflegen, am Handy (400 px) testen.
- Neue Quelle für den Scraper: Adapter in `scraper/adapters/` (oder `jsonld`/`ical` nutzen), gespeicherte Beispielseite unter `tests/fixtures/`, Test schreiben, dann in `data/sources.yaml` `enabled: true` setzen.
