"""Adapter lesen eine Kalenderseite und liefern Kandidaten.

Jeder Adapter ist ein Modul mit einer Funktion
    extract(html: str, url: str) -> list[dict]
die Kandidaten im Format
    {"title": str, "start": "JJJJ-MM-TT" | "JJJJ-MM-TTTHH:MM", "venue": str, "url": str}
zurückgibt. Kandidaten sind KEINE geprüften Termine: Sie landen in data/candidates.json
und werden vom wöchentlichen Lauf an der Stückseite verifiziert.

Neue Adapter: Datei scraper/adapters/<name>.py anlegen, in data/sources.yaml als
adapter: <name> eintragen, Test mit gespeicherter Seite unter tests/fixtures/ schreiben.
"""
from importlib import import_module


def load(name: str):
    return import_module(f"adapters.{name}")
