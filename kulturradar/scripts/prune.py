"""Räumt vergangene Termine und Fristen auf (täglich, deterministisch).

- entfernt vergangene Einzeltermine aus `dates`
- löscht Einträge ohne künftigen Termin und ohne laufende Zeitspanne
- löscht ❌-Einträge, deren `cancelledAt` älter als 7 Tage ist
- löscht Fristen mit Datum in der Vergangenheit (laufende Regeln bleiben)

Ausgabe: Zusammenfassung auf stdout (Markdown), Exit-Code 0.
"""
from __future__ import annotations

import datetime as dt
import sys

from common import future_dates, load, save, today


def prune(events: list[dict], deadlines: list[dict], ref: dt.date):
    removed, trimmed, kept = [], [], []
    for ev in events:
        rng = ev.get("range")
        fut = future_dates(ev, ref)
        if ev.get("status") == "cancel" and ev.get("cancelledAt"):
            if dt.date.fromisoformat(ev["cancelledAt"][:10]) <= ref - dt.timedelta(days=7):
                removed.append(ev["title"])
                continue
        if rng and rng.get("end") and rng["end"] >= ref.isoformat():
            if len(fut) != len(ev.get("dates") or []):
                trimmed.append(ev["title"])
            kept.append({**ev, "dates": fut})
            continue
        if not ev.get("dates") and not rng:
            kept.append(ev)  # "laufend" ohne Datum (z. B. Führungen nach Vereinbarung)
            continue
        if not fut:
            removed.append(ev["title"])
            continue
        if len(fut) != len(ev["dates"]):
            trimmed.append(ev["title"])
        kept.append({**ev, "dates": fut})
    dl_kept, dl_removed = [], []
    for d in deadlines:
        if d.get("date") and d["date"] < ref.isoformat() and d.get("kind") != "ongoing":
            dl_removed.append(d.get("title") or d.get("label"))
        else:
            dl_kept.append(d)
    return kept, removed, trimmed, dl_kept, dl_removed


def main() -> int:
    ref = today()
    ev_doc, dl_doc = load("events.json"), load("deadlines.json")
    kept, removed, trimmed, dl_kept, dl_removed = prune(ev_doc["events"], dl_doc["deadlines"], ref)
    changed = bool(removed or trimmed or dl_removed)
    if changed:
        stamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        save("events.json", {**ev_doc, "events": kept, "updated": stamp})
        save("deadlines.json", {**dl_doc, "deadlines": dl_kept, "updated": stamp})
    print(f"### Aufräumen {ref.isoformat()}")
    print(f"- Gelöscht (vergangen): {', '.join(removed) or '–'}")
    print(f"- Vergangene Einzeltermine gestrichen bei: {', '.join(trimmed) or '–'}")
    print(f"- Abgelaufene Fristen: {', '.join(dl_removed) or '–'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
