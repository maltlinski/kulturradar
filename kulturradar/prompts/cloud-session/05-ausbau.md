# Ideen für später

Jede Idee ist ein eigener Prompt. Kopiere nur die, die du willst, in die Cloud-Sitzung (nach `CLAUDE.md` lesen lassen).

**Merkliste geräteübergreifend.** „Die Merkliste liegt nur im localStorage. Baue einen Export/Import als Link: Die Merkliste wird als kurzer Code in einen Link kodiert (`…/#stars=<code>`), damit Malte sie vom Laptop aufs Handy bringen kann; beim Öffnen fragt die Seite, ob sie zusammengeführt werden soll. Kein Server, keine Anmeldung.“

**Persönlicher Feed der Merkliste.** „Erzeuge beim Klick auf ‚Merkliste in Kalender‘ eine `.ics`-Datei (gibt es schon). Ergänze einen Hinweis, dass Änderungen nur der abonnierte Gesamt-Feed automatisch nachzieht.“

**Benachrichtigung per Telegram.** „Ergänze im täglichen Lauf einen optionalen Schritt, der bei Auffälligkeiten (Absage, Ausverkauf, Frist in ≤ 3 Tagen) eine kurze Telegram-Nachricht schickt. Bot-Token und Chat-ID als Secrets `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`; ohne Secrets wird der Schritt übersprungen. Anleitung zum Anlegen des Bots für Malte schreiben.“

**Karte.** „Zeige in der Detailansicht einen Link ‚In Karten öffnen‘ (OpenStreetMap-Suche nach Ort und Stadt). Keine eingebettete Karte, keine externen Skripte.“

**Tanzfokus-Startseite.** „Füge über der Agenda einen Bereich ‚Für Profis‘ ein: Workshops, Masterclasses, Auditions, Calls und offene Proben der nächsten 8 Wochen plus alle Fristen dazu, kompakt.“

**Archiv-Statistik.** „Erzeuge aus der Git-Historie von `data/events.json` eine Seite ‚Rückblick‘: wie viele Vorstellungen pro Sparte und Stadt im Semester, welche besucht (Merkliste-Export als Eingabe). Nützlich für Maltes Kulturmanagement-Studium.“

**Quellen-Gesundheit.** „Erzeuge aus `reports/watch-*.md` eine kleine Übersicht: welche Quelle wie oft nicht erreichbar war, seit wann. Als Abschnitt im Wochen-PR.“
