"""Höflicher HTTP-Abruf: robots.txt beachten, pro Host langsam, klare Kennung."""
from __future__ import annotations

import time
import urllib.robotparser
from dataclasses import dataclass
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

USER_AGENT = "KulturradarBot/0.1 (privater Veranstaltungskalender; +https://github.com/maltlinski/kulturradar)"
DELAY_SECONDS = 4.0
TIMEOUT = 25

_robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
_last_hit: dict[str, float] = {}
_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "it,en;q=0.8,de;q=0.6"})


@dataclass
class Page:
    url: str
    ok: bool
    status: int | None
    html: str = ""
    error: str = ""

    def text(self) -> str:
        if not self.html:
            return ""
        soup = BeautifulSoup(self.html, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        return " ".join(soup.get_text(" ").split())


def allowed(url: str) -> bool:
    host = urlparse(url).scheme + "://" + urlparse(url).netloc
    if host not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = _session.get(host + "/robots.txt", timeout=TIMEOUT)
            if r.status_code >= 400:
                _robots[host] = None  # keine robots.txt -> erlaubt
            else:
                rp.parse(r.text.splitlines())
                _robots[host] = rp
        except requests.RequestException:
            _robots[host] = None
    rp = _robots[host]
    return True if rp is None else rp.can_fetch(USER_AGENT, url)


def get(url: str) -> Page:
    if not allowed(url):
        return Page(url, False, None, error="robots.txt verbietet den Abruf")
    host = urlparse(url).netloc
    wait = DELAY_SECONDS - (time.monotonic() - _last_hit.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    _last_hit[host] = time.monotonic()
    try:
        r = _session.get(url, timeout=TIMEOUT)
    except requests.RequestException as exc:
        return Page(url, False, None, error=type(exc).__name__)
    if r.status_code >= 400:
        return Page(url, False, r.status_code, error=f"HTTP {r.status_code}")
    r.encoding = r.encoding or r.apparent_encoding
    return Page(url, True, r.status_code, html=r.text)
