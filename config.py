from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from typing import Dict

import yaml


@dataclass
class KalshiConfig:
    environment: str = "demo"
    base_url: str = "https://demo-api.kalshi.co"
    email: str = ""
    password: str = ""
    api_key: str = ""


@dataclass
class ModelConfig:
    min_samples: int = 100
    random_state: int = 42


@dataclass
class RiskConfig:
    bankroll: float = 1000.0
    fractional_kelly: float = 0.25
    max_bankroll_per_trade: float = 0.02
    daily_loss_limit: float = 0.05
    max_concurrent_positions: int = 10
    max_exposure_per_sport: float = 0.2
    min_edge: float = 0.02


@dataclass
class TradingConfig:
    paper: bool = True
    retry_attempts: int = 3
    retry_delay_seconds: int = 1


@dataclass
class AppConfig:
    kalshi: KalshiConfig
    sports: Dict[str, bool]
    model: ModelConfig
    risk: RiskConfig
    trading: TradingConfig


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp) or {}


def load_config(path: str | Path = "config.yaml") -> AppConfig:
    raw = _load_yaml(Path(path))

    kalshi_raw = raw.get("kalshi", {})
    kalshi = KalshiConfig(
        environment=os.getenv("KALSHI_ENV", kalshi_raw.get("environment", "demo")),
        base_url=kalshi_raw.get("base_url", "https://demo-api.kalshi.co"),
        email=os.getenv("KALSHI_EMAIL", kalshi_raw.get("email", "")),
        password=os.getenv("KALSHI_PASSWORD", kalshi_raw.get("password", "")),
        api_key=os.getenv("KALSHI_API_KEY", kalshi_raw.get("api_key", "")),
    )

    sports = {
        "nba": True,
        "nfl": True,
        "mlb": True,
        "mma": True,
        "esports": True,
        "soccer": True,
    }
    sports.update(raw.get("sports", {}))

    model = ModelConfig(**raw.get("model", {}))
    risk = RiskConfig(**raw.get("risk", {}))
    trading = TradingConfig(**raw.get("trading", {}))

    return AppConfig(kalshi=kalshi, sports=sports, model=model, risk=risk, trading=trading)
