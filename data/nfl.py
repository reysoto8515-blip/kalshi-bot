from __future__ import annotations

from .cache import DataCache


def fetch_nfl_data(cache: DataCache | None = None) -> dict:
    cache = cache or DataCache()
    key = "nfl_stats"
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = {
        "sport": "nfl",
        "sources": ["espn", "nfl_data_py"],
        "team_stats": [],
        "player_stats": [],
        "injuries": [],
        "schedule": [],
    }
    cache.set(key, data)
    return data
