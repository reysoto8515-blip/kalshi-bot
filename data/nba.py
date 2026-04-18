from __future__ import annotations

from .cache import DataCache


def fetch_nba_data(cache: DataCache | None = None) -> dict:
    cache = cache or DataCache()
    key = "nba_stats"
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = {
        "sport": "nba",
        "sources": ["balldontlie", "nba_api"],
        "team_stats": [],
        "player_stats": [],
        "game_logs": [],
    }
    cache.set(key, data)
    return data
