import unittest

from engine.risk import PositionContext, RiskManager


class RiskTests(unittest.TestCase):
    def test_position_size_respects_cap(self):
        risk = RiskManager(
            bankroll=1000,
            fractional_kelly=1.0,
            max_bankroll_per_trade=0.02,
            daily_loss_limit=0.05,
            max_concurrent_positions=10,
            max_exposure_per_sport=0.2,
        )
        self.assertEqual(risk.position_size(0.8, 50), 20.0)

    def test_daily_loss_limit_blocks_trade(self):
        risk = RiskManager(
            bankroll=1000,
            fractional_kelly=0.25,
            max_bankroll_per_trade=0.02,
            daily_loss_limit=0.05,
            max_concurrent_positions=10,
            max_exposure_per_sport=0.2,
        )
        ctx = PositionContext(open_positions=1, sport_exposure=0.1, daily_pnl=-60)
        self.assertFalse(risk.can_open_position(ctx))


if __name__ == "__main__":
    unittest.main()
