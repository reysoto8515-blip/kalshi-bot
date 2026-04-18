import unittest

from main import main


class MainTests(unittest.TestCase):
    def test_scan_command_runs(self):
        code = main(["--config", "config.yaml", "scan"])
        self.assertEqual(code, 0)

    def test_backtest_command_runs(self):
        code = main(["--config", "config.yaml", "backtest"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
