from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Iterable

from kalshi.client import KalshiClient, TradeRequest
from engine.ev import MarketOpportunity


@dataclass
class ExecutionResult:
    market_id: str
    side: str
    count: int
    price_cents: int
    status: str
    message: str


class TradingExecutor:
    def __init__(self, client: KalshiClient, paper: bool = True, retry_attempts: int = 3, retry_delay_seconds: int = 1):
        self.client = client
        self.paper = paper
        self.retry_attempts = max(1, retry_attempts)
        self.retry_delay_seconds = max(0, retry_delay_seconds)

    def execute(self, opportunities: Iterable[MarketOpportunity], contract_count: int = 1) -> list[ExecutionResult]:
        results: list[ExecutionResult] = []
        for opp in opportunities:
            if self.paper:
                results.append(
                    ExecutionResult(
                        market_id=opp.market_id,
                        side=opp.side,
                        count=contract_count,
                        price_cents=opp.market_price_cents,
                        status="paper",
                        message="Simulated order (paper mode)",
                    )
                )
                continue

            trade = TradeRequest(
                market_id=opp.market_id,
                side=opp.side,
                action="buy",
                count=contract_count,
                price_cents=opp.market_price_cents,
            )

            last_error = ""
            for attempt in range(1, self.retry_attempts + 1):
                try:
                    self.client.place_trade(trade)
                    results.append(
                        ExecutionResult(
                            market_id=opp.market_id,
                            side=opp.side,
                            count=contract_count,
                            price_cents=opp.market_price_cents,
                            status="submitted",
                            message=f"Submitted on attempt {attempt}",
                        )
                    )
                    break
                except Exception as exc:  # pragma: no cover
                    last_error = str(exc)
                    if attempt < self.retry_attempts:
                        time.sleep(self.retry_delay_seconds)
            else:
                results.append(
                    ExecutionResult(
                        market_id=opp.market_id,
                        side=opp.side,
                        count=contract_count,
                        price_cents=opp.market_price_cents,
                        status="failed",
                        message=last_error or "Unknown order error",
                    )
                )
        return results
