from pathlib import Path
import unittest

from config import load_config


class ConfigTests(unittest.TestCase):
    def test_load_config_defaults(self):
        tmp_dir = Path("/tmp/kalshi-bot-tests")
        tmp_dir.mkdir(parents=True, exist_ok=True)
        cfg = tmp_dir / "config.yaml"
        cfg.write_text("sports:\n  nba: false\n", encoding="utf-8")
        loaded = load_config(cfg)
        self.assertFalse(loaded.sports["nba"])
        self.assertTrue(loaded.sports["nfl"])


if __name__ == "__main__":
    unittest.main()
