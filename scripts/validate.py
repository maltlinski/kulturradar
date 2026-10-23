"""Prüft data/*.json gegen das Schema und die Verifikationsregeln.

Fehler (Exit 1): Schema verletzt, doppelte IDs, ✅ ohne Beleg-Quelle, Top-Tipp ohne ✅.
Warnungen (Exit 0): z. B. Einträge ohne künftigen Termin (prune vergessen?).
Aufruf: python scripts/validate.py [--strict]   (--strict: Warnungen zählen als Fehler)
"""
from __future__ import annotations

import json
import sys

import jsonschema

from common import ROOT, future_dates, is_evidence, load, today


def check() -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    schema = json.loads((ROOT / "schema" / "data.schema.json").read_text(encoding="utf-8"))
    docs = {"events.json": load("events.json"), "deadlines.json": load("deadlines.json"), "meta.json": load("meta.json")}
    for name, doc in docs.items():
        sub = schema["$defs"][name.split(".")[0]]
        for err in jsonschema.Draft202012Validator({**sub, "$defs": schema["$defs"]}).iter_errors(doc):
            path = "/".join(str(p) for p in err.absolute_path)
            errors.append(f"{name}: {path}: {err.message}")
    events = docs["events.json"]["events"]
    ref = today()
    ids = {}
    for ev in events:
        if ev["id"] in ids:
            errors.append(f"doppelte ID: {ev['id']}")
        ids[ev["id"]] = ev
        has_evidence = any(is_evidence(s["url"], ev.get("region")) for s in ev.get("sources", []))
        if ev.get("status") in ("ok", "partial") and not has_evidence:
            errors.append(f"✅ ohne Beleg-Quelle (Tier 1/2 bzw. Trip-Quelle): {ev['id']}")
        if ev.get("status") == "cancel" and not ev.get("cancelledAt"):
            warnings.append(f"❌ ohne cancelledAt (wird nie automatisch gelöscht): {ev['id']}")
        dates = [o["date"] for o in ev.get("dates") or []]
        if dates != sorted(dates):
            warnings.append(f"dates nicht sortiert: {ev['id']}")
        rng = ev.get("range")
        if ev.get("dates") and not future_dates(ev, ref) and not (rng and rng.get("end", "") >= ref.isoformat()):
            warnings.append(f"kein künftiger Termin mehr (prune.py laufen lassen): {ev['id']}")
    for p in docs["meta.json"].get("topPicks", []):
        ev = ids.get(p["id"])
        if not ev:
            errors.append(f"Top-Tipp verweist auf unbekannte ID: {p['id']}")
        elif ev.get("status") != "ok":
            errors.append(f"Top-Tipp ist nicht ✅: {p['id']}")
    return errors, warnings


def main() -> int:
    strict = "--strict" in sys.argv
    errors, warnings = check()
    for w in warnings:
        print("WARNUNG:", w)
    for e in errors:
        print("FEHLER:", e)
    n = len(load("events.json")["events"])
    print(f"{n} Termine geprüft: {len(errors)} Fehler, {len(warnings)} Warnungen.")
    return 1 if errors or (strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
