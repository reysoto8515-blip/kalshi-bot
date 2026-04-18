from __future__ import annotations

from .cache import DataCache


def fetch_mlb_data(cache: DataCache | None = None) -> dict:
    cache = cache or DataCache()
    key = "mlb_stats"
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = {
        "sport": "mlb",
        "sources": ["mlb_stats_api"],
        "team_stats": [],
        "player_stats": [],
        "pitching_matchups": [],
    }
    cache.set(key, data)
    return data
