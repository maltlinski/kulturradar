Du arbeitest im Repository „kulturradar“, Maltes geprüftem Kulturkalender für Bologna. Lies zuerst `CLAUDE.md` und `README.md`. Antworte auf Deutsch.

Aufgabe: Das Repository einsatzbereit machen und die Seite zum ersten Mal über GitHub Pages veröffentlichen.

1. Umgebung prüfen: `pip install -r requirements.txt`, dann `python -m pytest -q tests`, `python scripts/validate.py`, `python scripts/build.py`. Alles muss grün sein. Behebe echte Fehler im Code; ändere keine Termindaten, um Prüfungen zu bestehen. Wenn `validate.py` einen Regelverstoß in `data/` meldet, setze den Eintrag nach den Regeln in `CLAUDE.md` auf 🟡 mit Begründung, statt die Regel aufzuweichen.
2. Platzhalter ersetzen: `OWNER` in `site/index.html` (meta name="repo") und in `scraper/fetch.py` (User-Agent) durch `<owner>/<repo>` dieses Repositorys ersetzen (aus `git remote get-url origin`).
3. Seite lokal prüfen: `_site/` mit `python -m http.server -d _site 8000` starten und mit einem Headless-Browser (Playwright, falls verfügbar) Screenshots bei 1280 px und 400 px Breite, hell und dunkel, machen. Prüfe: Termine werden geladen, Agenda/Woche/Monat schalten um, Filter wirken, Detailansicht öffnet, `.ics`-Download funktioniert, keine Konsolenfehler, kein horizontales Scrollen am Handy. Behebe, was kaputt ist.
4. GitHub Pages: Prüfe mit `gh api repos/{owner}/{repo}/pages`, ob Pages aktiv ist. Wenn nicht, versuche `gh api -X POST repos/{owner}/{repo}/pages -f build_type=workflow`. Klappt das nicht (fehlende Rechte), sag Malte genau, was er unter Settings → Pages einstellen muss (Source: GitHub Actions), und warte auf seine Bestätigung.
5. Änderungen auf einen Branch committen, PR öffnen, nach grünem Check mergen (oder Malte um den Merge bitten, falls du nicht mergen darfst). Danach den Workflow „Prüfen und veröffentlichen“ beobachten (`gh run watch`).
6. Ergebnis melden: URL der Seite, URLs der vier Kalender-Feeds (`kulturradar.ics`, `tanz.ics`, `ausfluege.ics`, `fristen.ics`) und eine kurze Anleitung, wie Malte einen Feed in Google Kalender und Apple Kalender abonniert (per URL abonnieren, nicht importieren).

Keine Änderungen an den Termindaten außer nach Schritt 1. Nichts an Workflows für den täglichen oder wöchentlichen Lauf ändern; das kommt in Schritt 03.
