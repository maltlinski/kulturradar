Du arbeitest im Repository „kulturradar“. Lies `CLAUDE.md`, `prompts/weekly-research.md` und die Workflows in `.github/workflows/`. Antworte auf Deutsch.

Ziel: Täglicher Lauf und wöchentliche Recherche laufen automatisch und sind einmal erfolgreich getestet.

1. **Workflows prüfen.** Gleiche `pages.yml`, `daily.yml` und `weekly-research.yml` mit der aktuellen Dokumentation ab, besonders:
   - `anthropics/claude-code-action`: aktuelle Hauptversion, Namen der Eingaben (`anthropic_api_key`, `prompt`, `claude_args`), Syntax für erlaubte Werkzeuge, benötigte Berechtigungen. Korrigiere Abweichungen.
   - Aufruf von `pages.yml` als wiederverwendbarer Workflow aus `daily.yml` (Berechtigungen, Concurrency).
   - Versionen von `actions/checkout`, `setup-python`, `upload-pages-artifact`, `deploy-pages`.
   Prüfe die Workflows mit `actionlint`, falls verfügbar.
2. **Täglichen Lauf testen.** `gh workflow run daily.yml`, mit `gh run watch` beobachten. Prüfe: Commit mit Bericht entstanden? Issue bei Auffälligkeiten? Seite neu veröffentlicht? Behebe Fehler und wiederhole, bis der Lauf grün ist.
3. **Wochenrecherche: Variante wählen.** Frag Malte, welche Variante er will, und erkläre kurz die Unterschiede:
   - **A) GitHub Action** mit eigenem API-Schlüssel: läuft komplett auf GitHub, kostet API-Nutzung (geschätzt wenige Euro pro Woche; schätze anhand von `--max-turns` und Seitenanzahl grob ab und sag, wie man ein Ausgabenlimit in der Anthropic-Konsole setzt). Malte muss das Secret `ANTHROPIC_API_KEY` anlegen.
   - **B) Geplante Claude-Sitzung** (wie der bisherige Montags-Task) mit Zugriff auf dieses Repository: keine extra API-Kosten, läuft über sein Claude-Abo. Dann `weekly-research.yml` auf nur `workflow_dispatch` umstellen (Zeitplan entfernen) und in `04-umstieg.md` den neuen Prompt für den geplanten Task verwenden.
4. **Bei Variante A:** Sobald das Secret existiert (`gh secret list`), `gh workflow run weekly-research.yml` starten und beobachten. Prüfe den entstandenen PR: Hält er die Regeln aus `CLAUDE.md` ein (Belege, keine erfundenen Uhrzeiten, Änderungsliste im PR-Text)? Wenn nicht, schärfe `prompts/weekly-research.md` nach. Den Test-PR nicht mergen, sondern Malte zur Durchsicht geben.
5. **Benachrichtigungen.** Erkläre Malte in zwei Sätzen, wie er GitHub-Benachrichtigungen für neue PRs und Issues dieses Repositorys aufs Handy bekommt (GitHub-App, „Watch“ → „Custom“: Issues, Pull requests).

Ergebnis melden: Status beider Läufe, Link zum Test-PR, offene Punkte.
