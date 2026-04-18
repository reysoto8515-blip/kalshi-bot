from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import math
from statistics import mean, pstdev
from typing import Iterable


@dataclass
class TradeRecord:
    timestamp: str
    sport: str
    market_id: str
    side: str
    contracts: int
    price_cents: int
    pnl: float


class PerformanceTracker:
    def __init__(self) -> None:
        self.trades: list[TradeRecord] = []

    def add_trade(self, trade: TradeRecord) -> None:
        self.trades.append(trade)

    def add_trades(self, trades: Iterable[TradeRecord]) -> None:
        self.trades.extend(trades)

    def summary(self) -> dict:
        if not self.trades:
            return {"trades": 0, "win_rate": 0.0, "roi": 0.0, "sharpe": 0.0, "pnl": 0.0}

        pnls = [t.pnl for t in self.trades]
        wins = sum(1 for p in pnls if p > 0)
        invested = sum((t.contracts * t.price_cents) / 100.0 for t in self.trades)
        total_pnl = sum(pnls)
        roi = (total_pnl / invested) if invested else 0.0
        std = pstdev(pnls) if len(pnls) > 1 else 0.0
        sharpe = (mean(pnls) / std) * math.sqrt(len(pnls)) if std > 0 else 0.0

        return {
            "trades": len(self.trades),
            "win_rate": wins / len(self.trades),
            "roi": roi,
            "sharpe": sharpe,
            "pnl": total_pnl,
        }

    def export_csv(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8", newline="") as fp:
            fieldnames = ["timestamp", "sport", "market_id", "side", "contracts", "price_cents", "pnl"]
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for trade in self.trades:
                writer.writerow(asdict(trade))
