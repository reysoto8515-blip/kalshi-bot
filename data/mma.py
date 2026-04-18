from __future__ import annotations

from .cache import DataCache


def fetch_mma_data(cache: DataCache | None = None) -> dict:
    cache = cache or DataCache()
    key = "mma_stats"
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = {
        "sport": "mma",
        "sources": ["ufcstats"],
        "fighters": [],
        "historical_fights": [],
    }
    cache.set(key, data)
    return data
