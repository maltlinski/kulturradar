"""Baut die statische Seite nach _site/ und erzeugt die Kalender-Feeds.

- _site/index.html, _site/data/*.json
- _site/kulturradar.ics  (alle künftigen Termine, ohne Ausflüge)
- _site/tanz.ics          (nur Tanz, Ballett, Workshops, offene Proben, inkl. Ausflüge)
- _site/ausfluege.ics     (nur Florenz, Mailand, Turin, Venedig)
- _site/fristen.ics       (Fristen als ganztägige Termine)
"""
from __future__ import annotations

import datetime as dt
import re
import shutil
import sys

from common import DATA, ROOT, future_dates, load, today

OUT = ROOT / "_site"
FOCUS = {"dance", "ballet", "workshop", "probe"}
CATLABEL = {"dance": "Tanz", "ballet": "Ballett", "workshop": "Workshop", "probe": "Offene Probe", "opera": "Oper",
            "theatre": "Theater", "music": "Musik", "social": "Social Dance", "tour": "Führung", "festival": "Festival",
            "art": "Ausstellung", "other": "Kultur"}


def esc(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")


def fold(line: str) -> str:
    """RFC 5545: Zeilen nach 75 Oktetten umbrechen."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not parts else 74):
            parts.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    parts.append(cur.decode("utf-8"))
    return "\r\n ".join(parts)


def plain(md: str) -> str:
    md = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", md or "")
    return re.sub(r"\*+", "", md)


def calendar(name: str, events: list[dict], ref: dt.date) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Kulturradar Bologna//DE", "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH", f"X-WR-CALNAME:{esc(name)}", "X-WR-TIMEZONE:Europe/Rome",
             "REFRESH-INTERVAL;VALUE=DURATION:PT12H", "X-PUBLISHED-TTL:PT12H",
             "BEGIN:VTIMEZONE", "TZID:Europe/Rome",
             "BEGIN:DAYLIGHT", "TZOFFSETFROM:+0100", "TZOFFSETTO:+0200", "TZNAME:CEST", "DTSTART:19700329T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU", "END:DAYLIGHT",
             "BEGIN:STANDARD", "TZOFFSETFROM:+0200", "TZOFFSETTO:+0100", "TZNAME:CET", "DTSTART:19701025T030000", "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU", "END:STANDARD",
             "END:VTIMEZONE"]
    for ev in events:
        for o in future_dates(ev, ref):
            d = o["date"].replace("-", "")
            times = re.findall(r"(\d{2}):(\d{2})", o.get("time") or "")
            slots = times or [None]
            for t in slots:
                uid = f"{ev['id']}-{d}{''.join(t) if t else ''}@kulturradar"
                lines += ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp}"]
                if t:
                    start = dt.datetime(int(d[:4]), int(d[4:6]), int(d[6:]), int(t[0]), int(t[1]))
                    end = start + dt.timedelta(hours=2)
                    lines += [f"DTSTART;TZID=Europe/Rome:{start:%Y%m%dT%H%M%S}", f"DTEND;TZID=Europe/Rome:{end:%Y%m%dT%H%M%S}"]
                else:
                    day = dt.date.fromisoformat(o["date"])
                    lines += [f"DTSTART;VALUE=DATE:{day:%Y%m%d}", f"DTEND;VALUE=DATE:{day + dt.timedelta(days=1):%Y%m%d}"]
                flags = [CATLABEL.get(ev["cat"], "")]
                if ev.get("free"): flags.append("gratis")
                if ev.get("discount"): flags.append("Rabatt")
                if ev.get("soldOut") == "full": flags.append("ausverkauft")
                if ev.get("status") in ("check", "partial"): flags.append("prüfen")
                if ev.get("status") == "cancel": flags.append("ABGESAGT")
                title = ev["title"] + (f" – {ev['artist']}" if ev.get("artist") else "")
                if ev.get("status") == "cancel":
                    title = "ABGESAGT: " + title
                desc = " · ".join(f for f in flags if f) + "\n" + (ev.get("when") or "") + "\n\n" + plain(ev.get("text", ""))
                if ev.get("sources"):
                    desc += "\n\nQuelle: " + ev["sources"][0]["url"]
                lines += [f"SUMMARY:{esc(title)}", f"LOCATION:{esc(', '.join(x for x in (ev.get('venue'), ev.get('city')) if x))}",
                          f"DESCRIPTION:{esc(desc)}", f"CATEGORIES:{esc(CATLABEL.get(ev['cat'], 'Kultur'))}"]
                if ev.get("sources"):
                    lines.append(f"URL:{ev['sources'][0]['url']}")
                if ev.get("status") == "cancel":
                    lines.append("STATUS:CANCELLED")
                lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


def deadline_calendar(deadlines: list[dict], ref: dt.date) -> str:
    evs = []
    for d in deadlines:
        if d.get("date") and d["date"] >= ref.isoformat():
            evs.append({"id": "frist-" + d["id"], "title": "Frist: " + d["title"], "artist": "", "cat": "other", "text": d.get("text", ""),
                        "when": d.get("label", ""), "dates": [{"date": d["date"], "time": None}], "venue": "", "city": "",
                        "status": d.get("status"), "sources": d.get("sources") or [], "free": d.get("free"), "discount": d.get("discount")})
    return calendar("Kulturradar – Fristen", evs, ref)


def main() -> int:
    ref = today()
    events = load("events.json")["events"]
    deadlines = load("deadlines.json")["deadlines"]
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "site", OUT)
    (OUT / "data").mkdir(exist_ok=True)
    for name in ("events.json", "deadlines.json", "meta.json"):
        shutil.copy(DATA / name, OUT / "data" / name)
    feeds = {
        "kulturradar.ics": calendar("Kulturradar Bologna", [e for e in events if e["region"] != "trip"], ref),
        "tanz.ics": calendar("Kulturradar – Tanz", [e for e in events if e["cat"] in FOCUS], ref),
        "ausfluege.ics": calendar("Kulturradar – Ausflüge", [e for e in events if e["region"] == "trip"], ref),
        "fristen.ics": deadline_calendar(deadlines, ref),
    }
    for name, body in feeds.items():
        (OUT / name).write_text(body, encoding="utf-8", newline="")
    (OUT / ".nojekyll").write_text("")
    n = sum(body.count("BEGIN:VEVENT") for body in feeds.values())
    print(f"_site gebaut: {len(events)} Einträge, {n} Kalendertermine in {len(feeds)} Feeds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
