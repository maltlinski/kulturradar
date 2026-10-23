# Umzug in eine Cloud-Sitzung mit GitHub-Zugriff

Diese Anleitung ist für dich, Malte. Die Dateien `01`–`05` sind Prompts, die du nacheinander in die Cloud-Sitzung kopierst. Jeder Prompt ist ein abgeschlossener Arbeitsschritt; warte jeweils, bis die Sitzung fertig ist und dir das Ergebnis zeigt.

## Vorbereitung (einmalig, ca. 10 Minuten)

1. **Repository anlegen:** Auf github.com ein neues Repository `kulturradar` anlegen (privat oder öffentlich, siehe unten). Ohne README, ohne .gitignore.
2. **Dateien hochladen:** Das ZIP entpacken. Entweder auf github.com „uploading an existing file“ wählen und den Inhalt des Ordners `kulturradar/` hineinziehen (inklusive des versteckten Ordners `.github`: auf dem Mac mit Cmd+Shift+. sichtbar machen), oder per Terminal:
   ```
   cd kulturradar
   git init -b main && git add . && git commit -m "Kulturradar v1"
   git remote add origin https://github.com/DEIN-NAME/kulturradar.git
   git push -u origin main
   ```
3. **Cloud-Sitzung starten:** In Claude Code (Web oder App) eine neue Cloud-Sitzung mit diesem Repository öffnen und GitHub-Zugriff erlauben.
4. Prompt `01-einrichten.md` hineinkopieren.

## Öffentlich oder privat?

Eine GitHub-Pages-Seite ist **immer öffentlich erreichbar**, auch aus einem privaten Repository (Zugriffsschutz gibt es nur bei GitHub Enterprise). Pages aus einem privaten Repository braucht außerdem ein kostenpflichtiges GitHub-Konto (Pro). Für einen Veranstaltungskalender ist ein öffentliches Repository meist die einfachste Wahl; persönliche Daten stehen darin nicht. Deine Merkliste bleibt ohnehin nur in deinem Browser.

## Reihenfolge

| Prompt | Was passiert | Dauer |
|---|---|---|
| `01-einrichten.md` | Repository prüfen, Tests, GitHub Pages einschalten, erste Veröffentlichung | kurz |
| `02-scraper-adapter.md` | Tägliche Quellenprüfung und Kalender-Scraper an den echten Seiten testen und einschalten | länger |
| `03-automatisierung.md` | Täglichen Lauf und wöchentliche Claude-Recherche einrichten und einmal testen | mittel |
| `04-umstieg.md` | Letzten Stand aus Notion übernehmen, alten Montags-Task umstellen | kurz |
| `05-ausbau.md` | Ideen für später, einzeln anstoßen | nach Bedarf |

## Was du selbst tun musst

- Bei `01`: GitHub Pages erlauben, falls die Sitzung es nicht selbst einschalten darf (Settings → Pages → Source: „GitHub Actions“).
- Bei `03`: Entscheiden, wie die Wochenrecherche läuft. Entweder als GitHub Action mit eigenem Anthropic-API-Schlüssel (Settings → Secrets and variables → Actions → `ANTHROPIC_API_KEY`), oder als geplante Claude-Sitzung mit Zugriff auf das Repository, ohne extra API-Kosten.
- Pull Requests des Wochenlaufs ansehen und mergen. Erst dann sind die Änderungen auf der Seite.
