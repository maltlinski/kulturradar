"""Tägliche Quellenprüfung für bekannte Termine.

Öffnet für jeden Eintrag mit Termin in den nächsten N Tagen (Standard 21) die Beleg-Quellen und meldet:
- Quelle nicht erreichbar / robots.txt verbietet Abruf
- Signalwörter für ausverkauft, letzte Plätze, abgesagt/verschoben/Streik
- Datum fehlt auf der Seite (Tag und Monat in keiner üblichen Schreibweise gefunden)
- Seite hat sich seit dem letzten Lauf geändert (Hash des Textes)

Ändert KEINE Daten. Schreibt einen Bericht nach reports/watch-JJJJ-MM-TT.md und gibt ihn aus.
Die Einordnung (Status setzen, ❌ markieren) macht der wöchentliche Claude-Lauf oder ein Mensch.

Aufruf: python scraper/watch.py [--days 21]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from common import DATA, ROOT, future_dates, is_evidence, load, sources_config, today  # noqa: E402

from fetch import get  # noqa: E402

CACHE = DATA / ".watch-cache.json"
MONTHS_IT = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
MONTHS_EN = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]


def date_patterns(iso: str) -> list[re.Pattern]:
    d = dt.date.fromisoformat(iso)
    day, mon = d.day, d.month
    return [
        re.compile(rf"\b0?{day}\s*[./-]\s*0?{mon}\b"),                         # 24.10 / 24/10
        re.compile(rf"\b0?{day}\s+{MONTHS_IT[mon-1]}\b", re.I),               # 24 ottobre
        re.compile(rf"\b0?{day}\s+{MONTHS_IT[mon-1][:3]}\b", re.I),           # 24 ott
        re.compile(rf"\b{MONTHS_EN[mon-1]}\s+0?{day}\b", re.I),               # October 24
        re.compile(rf"\b0?{day}\s+{MONTHS_EN[mon-1]}\b", re.I),               # 24 October
        re.compile(rf"\b{d.year}-{mon:02d}-{day:02d}\b"),                     # 2026-10-24
    ]


def scan(text: str, words: list[str]) -> list[str]:
    low = text.lower()
    return [w for w in words if w in low]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    args = ap.parse_args()
    ref = today()
    horizon = (ref + dt.timedelta(days=args.days)).isoformat()
    kw = sources_config().get("keywords", {})
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    events = load("events.json")["events"]

    findings: dict[str, list[str]] = {"unreachable": [], "cancel": [], "soldout": [], "few": [], "nodate": [], "changed": []}
    checked = 0
    for ev in events:
        fut = [o for o in future_dates(ev, ref) if o["date"] <= horizon]
        if not fut:
            continue
        urls = [s["url"] for s in ev.get("sources", []) if is_evidence(s["url"], ev.get("region"))][:2]
        for url in urls:
            checked += 1
            page = get(url)
            label = f"**{ev['title']}** ({ev['id']}) – [{url}]({url})"
            if not page.ok:
                findings["unreachable"].append(f"{label}: {page.error}")
                continue
            text = page.text()
            h = hashlib.sha256(text.encode()).hexdigest()[:16]
            if cache.get(url) and cache[url] != h:
                findings["changed"].append(label)
            cache[url] = h
            for key in ("cancel", "soldout", "few"):
                hits = scan(text, kw.get(key, []))
                if hits:
                    findings[key].append(f"{label}: „{'“, „'.join(hits)}“")
            missing = [o["date"] for o in fut if not any(p.search(text) for p in date_patterns(o["date"]))]
            if missing and len(missing) == len(fut):
                findings["nodate"].append(f"{label}: kein Datum gefunden für {', '.join(missing)}")

    CACHE.write_text(json.dumps(cache, indent=0, sort_keys=True))
    titles = {
        "cancel": "Mögliche Absage, Verschiebung oder Streik",
        "soldout": "Signalwort „ausverkauft“",
        "few": "Signalwort „letzte Plätze“",
        "nodate": "Datum nicht auf der Seite gefunden",
        "unreachable": "Quelle nicht erreichbar",
        "changed": "Seite seit dem letzten Lauf geändert",
    }
    lines = [f"# Quellenprüfung {ref.isoformat()}", "",
             f"{checked} Quellen geprüft für Termine bis {horizon}. Signalwörter können sich auf andere Termine derselben Seite beziehen: immer an der Seite selbst prüfen.", ""]
    total = 0
    for key in ("cancel", "soldout", "few", "nodate", "unreachable", "changed"):
        items = findings[key]
        if not items:
            continue
        total += len(items) if key != "changed" else 0
        lines += [f"## {titles[key]} ({len(items)})", *[f"- {x}" for x in items], ""]
    if total == 0:
        lines.append("Keine Auffälligkeiten.")
    report = "\n".join(lines) + "\n"
    out = ROOT / "reports"
    out.mkdir(exist_ok=True)
    (out / f"watch-{ref.isoformat()}.md").write_text(report, encoding="utf-8")
    print(report)
    # Exit 0 immer; der Workflow entscheidet anhand der Datei, ob ein Issue entsteht.
    (out / "watch-latest.json").write_text(json.dumps({"date": ref.isoformat(), "attention": total}), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
