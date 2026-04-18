from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PositionContext:
    open_positions: int
    sport_exposure: float
    daily_pnl: float


@dataclass
class RiskManager:
    bankroll: float
    fractional_kelly: float
    max_bankroll_per_trade: float
    daily_loss_limit: float
    max_concurrent_positions: int
    max_exposure_per_sport: float

    def kelly_fraction(self, win_probability: float, price_cents: int) -> float:
        if not 0 <= win_probability <= 1:
            raise ValueError("win_probability must be in [0, 1]")
        if not 1 <= price_cents <= 99:
            return 0.0

        b = (100 - price_cents) / price_cents
        q = 1 - win_probability
        kelly = (b * win_probability - q) / b if b > 0 else 0.0
        return max(0.0, kelly * self.fractional_kelly)

    def position_size(self, win_probability: float, price_cents: int) -> float:
        fraction = self.kelly_fraction(win_probability, price_cents)
        stake = self.bankroll * min(fraction, self.max_bankroll_per_trade)
        return round(max(0.0, stake), 2)

    def can_open_position(self, ctx: PositionContext) -> bool:
        if ctx.open_positions >= self.max_concurrent_positions:
            return False
        if ctx.sport_exposure >= self.max_exposure_per_sport:
            return False
        if ctx.daily_pnl <= -(self.bankroll * self.daily_loss_limit):
            return False
        return True
