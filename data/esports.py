from __future__ import annotations

from .cache import DataCache


def fetch_esports_data(cache: DataCache | None = None) -> dict:
    cache = cache or DataCache()
    key = "esports_stats"
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = {
        "sport": "esports",
        "sources": ["pandascore"],
        "titles": ["lol", "cs2", "valorant"],
        "team_stats": [],
        "match_history": [],
    }
    cache.set(key, data)
    return data
