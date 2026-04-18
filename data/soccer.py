from __future__ import annotations

from .cache import DataCache


def fetch_soccer_data(cache: DataCache | None = None) -> dict:
    cache = cache or DataCache()
    key = "soccer_stats"
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = {
        "sport": "soccer",
        "sources": ["football-data.org"],
        "team_stats": [],
        "standings": [],
        "fixtures": [],
    }
    cache.set(key, data)
    return data
