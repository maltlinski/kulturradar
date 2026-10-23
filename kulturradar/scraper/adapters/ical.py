"""Generischer Adapter für iCal-Feeds (.ics)."""
from __future__ import annotations

import datetime as dt

import icalendar


def extract(html: str, url: str) -> list[dict]:
    cal = icalendar.Calendar.from_ical(html)
    out = []
    for comp in cal.walk("VEVENT"):
        start = comp.decoded("DTSTART", None)
        if start is None:
            continue
        if isinstance(start, dt.datetime):
            start_s = start.strftime("%Y-%m-%dT%H:%M")
        else:
            start_s = start.isoformat()
        out.append({
            "title": str(comp.get("SUMMARY", "")).strip(),
            "start": start_s,
            "end": None,
            "venue": str(comp.get("LOCATION", "")),
            "url": str(comp.get("URL", url)),
            "status": str(comp.get("STATUS", "")) or None,
        })
    return out
