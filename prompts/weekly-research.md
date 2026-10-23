# Wochenlauf Kulturradar

Du pflegst den Kulturradar in diesem Repository. Lies zuerst `CLAUDE.md`; die Verifikationsregeln dort gelten strikt. Laufdatum ist heute (Europe/Rome); nutze es für alle Zeitberechnungen.

## Ablauf

1. **Stand laden.** `pip install -r requirements.txt` (falls nötig), dann `python scripts/prune.py` und `python scripts/validate.py`. Lies `data/events.json`, `data/deadlines.json`, `data/meta.json`, `data/candidates.json` und den neuesten Bericht in `reports/watch-*.md`. Lies offene Issues mit dem Label `quellenpruefung` (`gh issue list --label quellenpruefung`).

2. **Nachprüfen.** Öffne mit WebFetch für jeden Termin der nächsten 14 Tage und für jeden Eintrag mit `status` `check` oder `partial` die Beleg-Quelle. Prüfe Datum, Uhrzeit, Ort, Titel sowie ausverkauft, abgesagt, verschoben. Gehe jedem Hinweis aus dem Quellenbericht nach (Signalwörter, fehlendes Datum, geänderte Seite). In der ersten Woche jedes Monats (Tag 1–7) oder wenn „Vollprüfung erzwungen: true“ angegeben ist, prüfst du zusätzlich alle übrigen Einträge. Setze `lastChecked` auf das Laufdatum bei jedem geprüften Eintrag.

3. **Kandidaten verifizieren.** Für jeden Eintrag in `data/candidates.json`: Stückseite öffnen, nach den Regeln prüfen, passende Funde mit vollständigen Feldern in `data/events.json` übernehmen. Unpassendes (außerhalb der Region, kein Bezug zu den Prioritäten, Routine) weglassen.

4. **Neues finden.** Erst die Kalender der Tier-1-Quellen, dann die Tier-2-Portale, dann WebSearch mit diesen Begriffen (Monat und Jahr aktuell einsetzen): danza contemporanea Bologna [Monat] [Jahr] | spettacoli danza Emilia-Romagna [Monat] | masterclass danza gratuita Emilia-Romagna | audizioni danzatori Bologna | call coreografi Emilia-Romagna | workshop danza Bologna [Monat] | prima assoluta danza Reggio Emilia / Modena / Ferrara | stagione teatro Bologna novità | biglietti studenti universitari teatro Bologna | milonga Bologna | lindy hop Bologna serata. Horizont: 8 Wochen. Priorität wie in `CLAUDE.md`.

5. **Ausflugsziele.** Prüfe die Trip-Quellen für Florenz, Mailand, Turin, Venedig und suche mit: danza contemporanea Milano / Torino / Firenze / Venezia [Monat] [Jahr] | Teatro alla Scala balletto [Monat] | Torinodanza [Jahr] | MilanOltre [Jahr] | Fabbrica Europa [Jahr] | Teatro La Fenice [Monat] | Biennale Danza College [Jahr] call | audizioni danzatori Milano / Torino / Firenze. Hohe Messlatte, höchstens etwa 20 Einträge mit `region: trip`.

6. **Fristen.** Aktualisiere `data/deadlines.json`: Fristen der nächsten 14 Tage vollständig, wichtige spätere als `kind: outlook`.

7. **Speichern.**
   - `data/meta.json`: `version` +1, `lastCheck` = Laufdatum, `nextCheck` = Laufdatum + 7, `topPicks` = Top 3 der Woche (nur ✅, je ein Satz `why`), `briefUrl` = `https://github.com/<owner>/<repo>/blob/main/briefs/JJJJ-MM-TT.md`, `updated`.
   - Wochenbrief nach `briefs/JJJJ-MM-TT.md` (Vorlage unten).
   - `python scripts/validate.py` muss ohne Fehler laufen; `python scripts/build.py` muss durchlaufen.
   - Committen, Branch pushen, Pull Request öffnen.

## Pull Request

Titel: `Wochenlauf JJJJ-MM-TT: N geprüft, X neu, Y geändert`

Text (Markdown):
- **Wichtigstes** in 2–3 Sätzen (Fristen der nächsten 7 Tage zuerst).
- **Änderungen**: je Zeile „Titel: alter Wert → neuer Wert (Quelle)“.
- **Neu aufgenommen**: Titel, Datum, Ort, Status.
- **Gelöscht (vergangen)**: eine Zeile.
- **Nicht erreichbar**: Quellen mit Datum.
- **Prüfstatistik**: geprüft / ✅ / 🟡 / ❌ / nicht erreichbar.

## Wochenbrief-Vorlage (höchstens eine Bildschirmseite)

```
# Kulturradar · Woche ab TT.MM.JJJJ

1. Top 3 dieser Woche (nur ✅, je ein Satz warum, mit Link)
2. Die nächsten 14 Tage (Tabelle: Datum | Veranstaltung | Ort | Status, mit Link)
3. Neu angekündigt (Wochen 3–8)
4. Ausflugstipps Florenz / Mailand / Turin / Venedig (höchstens 3, nur ✅; weglassen, wenn nichts die Messlatte erfüllt)
5. Fristen & Anmeldungen
6. Änderungen & Absagen
7. Offene Prüfpunkte
8. Prüfstatistik (geprüft / ✅ / 🟡 / ❌ / Quellen nicht erreichbar)
```
Kostenlose Termine mit „gratis“, Studi- und Under-30/35-Tarife mit „Rabatt“ markieren.

## Grenzen

Nichts kaufen, Malte nirgends anmelden, niemandem schreiben. Keine Änderungen an `site/`, `scripts/`, `scraper/` oder Workflows in diesem Lauf; Verbesserungsideen als Abschnitt „Vorschläge“ an den PR-Text anhängen.
