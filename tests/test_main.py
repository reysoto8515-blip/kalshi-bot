import tempfile
from pathlib import Path
import unittest

from main import main


class MainTests(unittest.TestCase):
    def _make_config(self) -> str:
        tmp_dir = Path(tempfile.mkdtemp(prefix="kalshi-bot-main-tests-"))
        cfg = tmp_dir / "config.yaml"
        cfg.write_text(
            """
kalshi:
  environment: demo
  base_url: https://demo-api.kalshi.co
sports:
  nba: true
  nfl: true
  mlb: true
  mma: true
  esports: true
  soccer: true
risk:
  min_edge: 0.02
""".strip()
            + "\n",
            encoding="utf-8",
        )
        return str(cfg)

    def test_scan_command_runs(self):
        code = main(["--config", self._make_config(), "scan"])
        self.assertEqual(code, 0)

    def test_backtest_command_runs(self):
        code = main(["--config", self._make_config(), "backtest"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
