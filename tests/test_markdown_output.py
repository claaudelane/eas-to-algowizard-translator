import os
import tempfile
import unittest
import parse_strategy
import parse_collection


class MarkdownOutputTest(unittest.TestCase):
    def minimal_strategy_dict(self):
        return {
            "symbol": "EURUSD",
            "timeframe": "M5",
            "entry_conditions": [],
            "exit_conditions": [],
            "stop_loss": 0,
            "take_profit": 0,
            "position_size": 1,
            "direction": "Long",
            "optimization": {},
            "backtest": {},
        }

    def minimal_collection_dict(self):
        return {
            "symbol": "EURUSD",
            "timeframe": "M30",
            "entry_conditions": [],
            "exit_conditions": [],
            "stop_loss": 0,
            "take_profit": 0,
            "position_size": 1,
            "direction": "Long",
            "magic_number": 123,
            "opposite_entry_signal": False,
            "is_trailing_stop": False,
            "backtest_stats": {},
        }

    def test_markdown_no_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            current = os.getcwd()
            try:
                os.chdir(tmpdir)
                parse_strategy.to_markdown(self.minimal_strategy_dict(), "strategy.md")
                self.assertTrue(os.path.exists("strategy.md"))

                parse_collection.to_markdown(self.minimal_collection_dict(), "collection.md")
                self.assertTrue(os.path.exists("collection.md"))
            finally:
                os.chdir(current)


if __name__ == "__main__":
    unittest.main()
