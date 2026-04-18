from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import time
from typing import Any


@dataclass
class DataCache:
    cache_dir: Path = Path(".cache")
    ttl_seconds: int = 1800

    def __post_init__(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path_for(self, key: str) -> Path:
        safe_key = key.replace("/", "_").replace(" ", "_")
        return self.cache_dir / f"{safe_key}.json"

    def get(self, key: str) -> Any | None:
        path = self._path_for(key)
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as fp:
            payload = json.load(fp)
        expires_at = payload.get("expires_at", 0)
        if expires_at < time.time():
            return None
        return payload.get("data")

    def set(self, key: str, data: Any) -> None:
        path = self._path_for(key)
        payload = {"expires_at": time.time() + self.ttl_seconds, "data": data}
        with path.open("w", encoding="utf-8") as fp:
            json.dump(payload, fp)
