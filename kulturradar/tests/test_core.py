import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scraper"))

import build  # noqa: E402
import prune  # noqa: E402
from adapters import jsonld  # noqa: E402
from common import is_evidence  # noqa: E402
from discover import known  # noqa: E402
from watch import date_patterns  # noqa: E402


def ev(**kw):
    base = {"id": "x-2026-10-24", "title": "Témoin", "artist": "Collectif FAIR-E", "text": "", "when": "", "dates": [],
            "range": None, "venue": "Teatro Valli", "city": "Reggio Emilia", "sparte": "Tanz", "cat": "dance",
            "region": "er", "status": "ok", "statusNote": "✅", "free": False, "discount": False, "premiere": False,
            "soldOut": None, "sources": [{"label": "iteatri", "url": "https://www.iteatri.re.it/x"}]}
    base.update(kw)
    return base


REF = dt.date(2026, 10, 25)


def test_prune_trims_and_removes():
    events = [
        ev(id="a", dates=[{"date": "2026-10-24", "time": "20:00"}, {"date": "2026-10-26", "time": "20:00"}]),
        ev(id="b", dates=[{"date": "2026-10-20", "time": None}]),
        ev(id="c", dates=[], range={"start": "2026-10-01", "end": "2026-11-07"}),
        ev(id="d", dates=[], range=None),
        ev(id="e", dates=[{"date": "2026-11-01", "time": None}], status="cancel", cancelledAt="2026-10-15"),
    ]
    kept, removed, trimmed, _, _ = prune.prune(events, [], REF)
    ids = [e["id"] for e in kept]
    assert ids == ["a", "c", "d"]
    assert kept[0]["dates"] == [{"date": "2026-10-26", "time": "20:00"}]
    assert "Témoin" in trimmed and len(removed) == 2


def test_prune_deadlines():
    dls = [{"date": "2026-10-20", "kind": "date", "title": "alt"}, {"date": None, "kind": "ongoing", "title": "Regel"},
           {"date": "2026-10-26", "kind": "until", "title": "neu"}]
    _, _, _, kept, removed = prune.prune([], dls, REF)
    assert [d["title"] for d in kept] == ["Regel", "neu"] and removed == ["alt"]


def test_evidence_domains():
    assert is_evidence("https://www.tcbo.it/eventi/x/")
    assert is_evidence("https://stagione2027.tcbo.it/")
    assert not is_evidence("https://www.bolognatoday.it/x")
    assert not is_evidence("https://www.teatroallascala.org/x")
    assert is_evidence("https://www.teatroallascala.org/x", "trip")


def test_ics_has_timezone_and_two_slots():
    e = ev(dates=[{"date": "2026-11-15", "time": "16:30 + 20:30"}])
    body = build.calendar("Test", [e], REF)
    assert body.count("BEGIN:VEVENT") == 2
    assert "DTSTART;TZID=Europe/Rome:20261115T163000" in body
    assert all(len(line.encode()) <= 75 for line in body.split("\r\n"))


def test_jsonld_adapter():
    html = """<script type="application/ld+json">{"@context":"https://schema.org","@graph":[
      {"@type":"DanceEvent","name":"Notte Morricone","startDate":"2026-11-28T20:30:00+01:00",
       "location":{"@type":"Place","name":"Teatro EuropAuditorium"},"url":"/eventi/morricone/"}]}</script>"""
    out = jsonld.extract(html, "https://www.tcbo.it/")
    assert out == [{"title": "Notte Morricone", "start": "2026-11-28T20:30", "end": None, "venue": "Teatro EuropAuditorium",
                    "url": "https://www.tcbo.it/eventi/morricone/", "status": None}]


def test_known_matching():
    events = [ev(title="Notte Morricone", artist="Aterballetto", dates=[{"date": "2026-11-28", "time": "20:30"}])]
    assert known({"title": "Aterballetto – Notte Morricone", "start": "2026-11-28T20:30"}, events)
    assert not known({"title": "Giselle", "start": "2026-11-28"}, events)


def test_date_patterns():
    pats = date_patterns("2026-10-24")
    for s in ["sabato 24 ottobre", "24.10.2026", "24/10", "October 24", "24 ott"]:
        assert any(p.search(s) for p in pats), s
    assert not any(p.search("4 ottobre") for p in pats)
