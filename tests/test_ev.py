import unittest

from engine.ev import MarketOpportunity, calculate_expected_value, find_positive_ev


class EVTests(unittest.TestCase):
    def test_calculate_expected_value_positive(self):
        self.assertAlmostEqual(calculate_expected_value(0.60, 50), 0.10, places=6)

    def test_find_positive_ev_sorted(self):
        opportunities = [
            MarketOpportunity("nba", "a", "yes", 0.55, 50, 0.5),
            MarketOpportunity("nfl", "b", "yes", 0.65, 50, 0.4),
            MarketOpportunity("mlb", "c", "yes", 0.52, 52, 0.7),
        ]
        filtered = find_positive_ev(opportunities, 0.02)
        self.assertEqual([o.market_id for o in filtered], ["b", "a"])


if __name__ == "__main__":
    unittest.main()
