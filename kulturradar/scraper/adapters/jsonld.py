"""Generischer Adapter: liest schema.org-Events aus <script type="application/ld+json">."""
from __future__ import annotations

import json
from urllib.parse import urljoin

from bs4 import BeautifulSoup

EVENT_TYPES = {"Event", "TheaterEvent", "DanceEvent", "MusicEvent", "ScreeningEvent", "Festival", "EducationEvent", "ExhibitionEvent"}


def _walk(node):
    if isinstance(node, list):
        for x in node:
            yield from _walk(x)
    elif isinstance(node, dict):
        t = node.get("@type")
        types = set(t) if isinstance(t, list) else {t}
        if types & EVENT_TYPES:
            yield node
        for key in ("@graph", "subEvent", "itemListElement", "item", "event", "events"):
            if key in node:
                yield from _walk(node[key])


def _venue(loc) -> str:
    if isinstance(loc, list):
        loc = loc[0] if loc else {}
    if isinstance(loc, dict):
        if loc.get("name"):
            return str(loc["name"])
        addr = loc.get("address")
        return str(addr.get("addressLocality", "")) if isinstance(addr, dict) else str(addr or "")
    return str(loc or "")


def extract(html: str, url: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or tag.get_text() or "")
        except (json.JSONDecodeError, TypeError):
            continue
        for ev in _walk(data):
            start = str(ev.get("startDate") or "")[:16]
            name = str(ev.get("name") or "").strip()
            if not (start and name):
                continue
            out.append({
                "title": name,
                "start": start,
                "end": str(ev.get("endDate") or "")[:16] or None,
                "venue": _venue(ev.get("location")),
                "url": urljoin(url, ev.get("url") or url),
                "status": str(ev.get("eventStatus") or "").rsplit("/", 1)[-1] or None,
            })
    return out
