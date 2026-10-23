"""Gemeinsame Hilfsfunktionen für Skripte, Scraper und Tests."""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TZ = ZoneInfo("Europe/Rome")

CATS = {"dance", "ballet", "workshop", "probe", "opera", "theatre", "music", "social", "tour", "festival", "art", "other"}
STATUSES = {"ok", "check", "partial", "cancel"}


def today() -> dt.date:
    """Laufdatum. Mit KR_TODAY=JJJJ-MM-TT überschreibbar (Tests, Nachholläufe)."""
    forced = os.environ.get("KR_TODAY")
    if forced:
        return dt.date.fromisoformat(forced)
    return dt.datetime.now(TZ).date()


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name: str, obj) -> None:
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def sources_config() -> dict:
    return yaml.safe_load((DATA / "sources.yaml").read_text(encoding="utf-8"))


def _domain_set(items) -> set[str]:
    return {d.lower().removeprefix("www.") for d in items}


def evidence_domains(region: str | None = None) -> set[str]:
    """Domains, die als Beleg zählen (Tier 1 + 2, bei Ausflügen die Trip-Quellen)."""
    cfg = sources_config()
    if region == "trip":
        out: set[str] = set()
        for lst in cfg.get("trips", {}).values():
            out |= _domain_set(lst)
        return out
    return _domain_set(cfg.get("tier1", [])) | _domain_set(cfg.get("tier2", []))


def domain_of(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def is_evidence(url: str, region: str | None = None) -> bool:
    host = domain_of(url)
    return any(host == d or host.endswith("." + d) for d in evidence_domains(region))


def future_dates(ev: dict, ref: dt.date) -> list[dict]:
    return [o for o in ev.get("dates") or [] if o["date"] >= ref.isoformat()]
