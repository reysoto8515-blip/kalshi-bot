from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarketOpportunity:
    sport: str
    market_id: str
    side: str
    model_probability: float
    market_price_cents: int
    confidence: float

    @property
    def ev(self) -> float:
        return calculate_expected_value(self.model_probability, self.market_price_cents)


def implied_probability(price_cents: int) -> float:
    if price_cents < 0 or price_cents > 100:
        raise ValueError("price_cents must be in [0, 100]")
    return price_cents / 100.0


def calculate_expected_value(model_probability: float, price_cents: int, payout_cents: int = 100) -> float:
    if not 0 <= model_probability <= 1:
        raise ValueError("model_probability must be in [0, 1]")
    cost = price_cents / 100.0
    payout = payout_cents / 100.0
    return model_probability * payout - cost


def find_positive_ev(opportunities: list[MarketOpportunity], min_ev: float) -> list[MarketOpportunity]:
    return sorted(
        [opp for opp in opportunities if opp.ev >= min_ev],
        key=lambda opp: (opp.ev, opp.confidence),
        reverse=True,
    )
