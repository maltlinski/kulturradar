Du arbeitest im Repository „kulturradar“. Lies `CLAUDE.md`, `data/sources.yaml`, `scraper/fetch.py`, `scraper/watch.py`, `scraper/discover.py` und `scraper/adapters/`. Antworte auf Deutsch.

Ziel: Die automatische Suche funktioniert an den echten Seiten. Der Scraper liefert zuverlässig Kandidaten und Warnungen; geprüft und veröffentlicht wird weiterhin nach den Regeln in `CLAUDE.md`.

Teil A – Quellenprüfung (`watch.py`)
1. Lauf `python scraper/watch.py --days 21` aus. Werte den Bericht in `reports/` aus: Welche Quellen sind nicht erreichbar (robots.txt, HTTP-Fehler, Bot-Schutz)? Welche Signalwörter sind Fehlalarme (z. B. „sold out“ für andere Termine derselben Seite, Cookie-Banner, Menütexte)?
2. Verbessere die Erkennung, ohne Abrufe aggressiver zu machen: z. B. Text nur aus dem Hauptinhalt (`main`, `article`) lesen, Signalwörter nur in der Nähe des Datums werten, Fehlalarm-Muster ausschließen. Für jede Änderung einen Test mit gespeicherter Seite unter `tests/fixtures/` (HTML gekürzt auf das Nötige).
3. Seiten, die nur per JavaScript Inhalte laden (z. B. cartellone.emiliaromagnacultura.it), erkennen und im Bericht als „braucht Browser“ markieren. Playwright nur einführen, wenn es wirklich nötig ist, und dann als optionalen Schritt im Workflow.

Teil B – Kalender-Scraper (`discover.py`)
Gehe die Kalenderquellen in `data/sources.yaml` in dieser Reihenfolge durch: TCBO, Teatro Duse, ERT Bologna, I Teatri Reggio Emilia, Teatro Comunale Modena, Teatro Comunale Ferrara, Teatro Regio Parma, Gender Bender, Teatro Celebrazioni, Bologna Jazz Festival, ERT Modena. Für jede:
1. Seite einmal abrufen (robots.txt beachten) und speichern. Prüfen, ob sie schema.org-Events (JSON-LD), einen iCal-Feed oder eine stabile HTML-Struktur hat. Notiere das Ergebnis als Kommentar in `sources.yaml`.
2. Passenden Adapter wählen: `jsonld`, `ical` oder einen eigenen Adapter `scraper/adapters/<name>.py` mit `extract(html, url)`. Eigene Adapter sollen robust sein: lieber wenige sichere Felder (Titel, Datum, Link) als viele geratene. Keine Uhrzeiten oder Preise erraten.
3. Test mit der gespeicherten Seite schreiben (erwartete Anzahl, Stichproben von Titel und Datum).
4. Erst wenn der Test grün ist: `enabled: true`.
Wenn eine Quelle sich nicht sinnvoll scrapen lässt, `enabled: false` lassen und den Grund notieren. Tier-3-Seiten nie als Quelle für Kandidaten verwenden.

Teil C – Abschluss
1. `python scraper/discover.py` laufen lassen und `data/candidates.json` kurz zusammenfassen: Wie viele Kandidaten, wie viele davon plausibel neu, wie viele Doppelungen (Matching in `known()` ggf. verbessern, mit Test).
2. Alles als PR mit einer Tabelle „Quelle | Methode | Status | Bemerkung“. Kandidaten NICHT in `events.json` übernehmen; das macht der Wochenlauf nach Prüfung.

Höflichkeit bleibt Pflicht: `DELAY_SECONDS` nicht unter 3 senken, keine parallelen Abrufe, nur Seiten, die für die Termine nötig sind.
