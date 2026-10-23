Du arbeitest im Repository „kulturradar“. Lies `CLAUDE.md`. Antworte auf Deutsch.

Ziel: Das Repository wird die einzige Quelle der Wahrheit. Notion und die bisherige Claude-Web-App werden abgelöst, ohne dass Daten verloren gehen.

1. **Letzten Notion-Stand übernehmen.** Falls diese Sitzung den Notion-Connector hat: Lade die Seite „Kulturradar Master“ (https://app.notion.com/p/3d808b49560881079936eb01ea9a625b). Gleiche sie mit `data/events.json` und `data/deadlines.json` ab: Termine, die in Notion neuer sind (höhere Version, spätere Prüfung), übernimmst du mit allen Feldern; bestehende IDs bleiben. Übernimm auch die offenen Prüfpunkte als Issues mit Label `pruefpunkt`. Ohne Notion-Connector: Malte bitten, die Master-Seite als Markdown zu exportieren und hochzuladen, oder diesen Schritt überspringen, wenn er bestätigt, dass seit dem 19.10.2026 kein Notion-Lauf mehr stattgefunden hat. Änderungen als PR.
2. **Alten Montags-Task umstellen.** Der bisherige geplante Task „Kulturradar Bologna – Wochenlauf“ schreibt nach Notion und in die Datenbank der Claude-Web-App. Erkläre Malte, dass er ihn in Claude unter den geplanten Aufgaben deaktivieren oder ersetzen soll, sobald der neue Wochenlauf einmal erfolgreich war. Doppelte Läufe vermeiden.
3. **Falls Variante B (geplante Claude-Sitzung) gewählt wurde:** Gib Malte den folgenden Prompt für den neuen geplanten Task, mit Zugriff auf dieses Repository, wöchentlich montags ca. 7 Uhr:

   > Du pflegst den Kulturradar im Repository <owner>/kulturradar. Lies CLAUDE.md und prompts/weekly-research.md und führe den Wochenlauf vollständig aus. Arbeite auf einem neuen Branch recherche/JJJJ-MM-TT, öffne am Ende einen Pull Request gegen main. Sende eine Push-Benachrichtigung nur, wenn eine Frist in den nächsten 7 Tagen abläuft, ein Termin der nächsten 14 Tage abgesagt oder ausverkauft ist, ein sehr passender Profi-Workshop/Call/Audition neu ist, oder der Lauf gescheitert ist; erster Satz = das Wichtigste, danach Link zum PR.

4. **Verweise aktualisieren.** In `data/meta.json` `masterUrl` und `appUrl` entfernen, sobald Notion und die Web-App nicht mehr gepflegt werden; in `README.md` den Abschnitt „Herkunft der Daten“ aktualisieren. Malte einen Satz geben, den er oben in die Notion-Seite schreiben kann („Archiv, aktuell unter <Pages-URL>“). Die Claude-Web-App nicht löschen; das entscheidet Malte.

Ergebnis melden: was übernommen wurde, welche Schritte Malte selbst erledigen muss.
