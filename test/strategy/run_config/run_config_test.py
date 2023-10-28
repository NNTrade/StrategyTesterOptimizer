from dataclasses import FrozenInstanceError
import unittest
import logging
from src.strategy.run_config import RunConfig, date, MarketConfig, StrategyConfig


class RunConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_construct_THEN_construct_correctly(self):
        # Array
        rc = RunConfig(MarketConfig(("A", "B"), date(2020, 1, 1),
                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))
        # Act

        # Assert
        self.assertEqual(2, len(rc.market_cfg.stocks))
        self.assertIn("A", rc.market_cfg.stocks)
        self.assertIn("B", rc.market_cfg.stocks)
        self.assertEqual(date(2020, 1, 1), rc.market_cfg.from_date)
        self.assertEqual(date(2021, 1, 1), rc.market_cfg.untill_date)
        self.assertEqual(2, len(rc.strategy_cfg.keys()))
        self.assertEqual(1, rc.strategy_cfg["p1"])
        self.assertEqual(2, rc.strategy_cfg["p2"])

    def test_WHEN_construct_THEN_it_is_imutable(self):
        # Array
        rc = RunConfig(MarketConfig(["A", "B"], date(2020, 1, 1),
                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))

        # Act

        with self.assertRaises(AttributeError):
            rc.market_cfg.stocks = ['C']
        with self.assertRaises(AttributeError):
            rc.market_cfg.from_date = date(2020, 1, 2)
        with self.assertRaises(AttributeError):
            rc.market_cfg.untill_date = date(2021, 1, 2)
        with self.assertRaises(Exception):
            rc.strategy_cfg["p1"] = 2
        with self.assertRaises(AttributeError):
            rc.strategy_cfg = {"p3": 3}

        # Assert
        self.assertEqual(2, len(rc.market_cfg.stocks))
        self.assertIn("A", rc.market_cfg.stocks)
        self.assertIn("B", rc.market_cfg.stocks)
        self.assertEqual(date(2020, 1, 1), rc.market_cfg.from_date)
        self.assertEqual(date(2021, 1, 1), rc.market_cfg.untill_date)
        self.assertEqual(2, len(rc.strategy_cfg.keys()))
        self.assertEqual(1, rc.strategy_cfg["p1"])
        self.assertEqual(2, rc.strategy_cfg["p2"])

    def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
        # Array
        rc1 = RunConfig(MarketConfig(["A", "B"], date(2020, 1, 1),
                        date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))
        rc2 = RunConfig(MarketConfig(["A", "B"], date(2020, 1, 1),
                        date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))
        # Act

        # Assert
        self.assertEqual(hash(rc1), hash(rc2))
        self.assertEqual(rc1, rc2)
    