"""Sucht auf den Kalenderseiten aus data/sources.yaml nach Terminen, die noch nicht erfasst sind.

Ergebnis: data/candidates.json (wird bei jedem Lauf neu geschrieben). Kandidaten sind ungeprüft
und erscheinen NICHT auf der Seite. Der wöchentliche Claude-Lauf verifiziert sie an der Stückseite
und übernimmt passende nach events.json.

Aufruf: python scraper/discover.py [--weeks 8] [--all]   (--all: auch enabled:false-Quellen versuchen)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from common import load, save, sources_config, today  # noqa: E402

import adapters  # noqa: E402
from fetch import get  # noqa: E402


def norm(s: str) -> set[str]:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    stop = {"di", "del", "della", "il", "la", "le", "lo", "e", "the", "a", "and", "und", "der", "die", "das", "in", "per", "con"}
    return {w for w in re.findall(r"[a-z0-9]{3,}", s) if w not in stop}


def known(cand: dict, events: list[dict]) -> bool:
    words = norm(cand["title"])
    day = cand["start"][:10]
    for ev in events:
        if not any(o["date"] == day for o in ev.get("dates") or []):
            continue
        ev_words = norm(ev["title"] + " " + ev.get("artist", ""))
        if words and len(words & ev_words) / len(words) >= 0.5:
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weeks", type=int, default=8)
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    ref = today()
    horizon = (ref + dt.timedelta(weeks=args.weeks)).isoformat()
    events = load("events.json")["events"]
    found, report = [], []
    for cal in sources_config().get("calendars", []):
        if not cal.get("enabled") and not args.all:
            continue
        page = get(cal["url"])
        if not page.ok:
            report.append(f"- {cal['name']}: nicht erreichbar ({page.error})")
            continue
        try:
            items = adapters.load(cal.get("adapter", "jsonld")).extract(page.html, cal["url"])
        except Exception as exc:  # Adapter-Fehler sollen den Lauf nicht abbrechen
            report.append(f"- {cal['name']}: Adapter-Fehler {type(exc).__name__}: {exc}")
            continue
        fresh = [c for c in items if ref.isoformat() <= c["start"][:10] <= horizon and not known(c, events)]
        for c in fresh:
            c["source"] = cal["name"]
            c["foundAt"] = ref.isoformat()
        found += fresh
        report.append(f"- {cal['name']}: {len(items)} Termine gelesen, {len(fresh)} neu")
    found.sort(key=lambda c: c["start"])
    save("candidates.json", {"generated": ref.isoformat(), "candidates": found})
    print(f"### Discovery {ref.isoformat()}")
    print("\n".join(report) or "- keine Kalenderquelle aktiv (enabled: true in data/sources.yaml setzen)")
    print(f"\n{len(found)} Kandidaten nach data/candidates.json geschrieben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
