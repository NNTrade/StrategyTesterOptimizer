import unittest
import logging
from src.strategy.run_config import RunConfig, date, MarketConfig, StrategyConfig, StrategyId, StockConfig, TimeFrame

class RunConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_construct_THEN_construct_correctly(self):
        # Array
        si = StrategyId("test", "0.0.1")
        s1 = StockConfig("A", TimeFrame.D)
        s2 = StockConfig("B", TimeFrame.D)
        rc = RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))
        # Act

        # Assert
        self.assertEqual(si, rc.strategy_id)
        self.assertEqual(2, len(rc.market_cfg.stocks))
        self.assertIn(s1, rc.market_cfg.stocks)
        self.assertIn(s2, rc.market_cfg.stocks)
        self.assertEqual(date(2020, 1, 1), rc.market_cfg.from_date)
        self.assertEqual(date(2021, 1, 1), rc.market_cfg.untill_date)
        self.assertEqual(2, len(rc.strategy_cfg.keys()))
        self.assertEqual(1, rc.strategy_cfg["p1"])
        self.assertEqual(2, rc.strategy_cfg["p2"])

    def test_WHEN_construct_THEN_it_is_imutable(self):
        # Array
        si = StrategyId("test", "0.0.1")
        s1 = StockConfig("A", TimeFrame.D)
        s2 = StockConfig("B", TimeFrame.D)
        rc = RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
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
        self.assertEqual(si, rc.strategy_id)
        self.assertEqual(2, len(rc.market_cfg.stocks))
        self.assertIn(s1, rc.market_cfg.stocks)
        self.assertIn(s2, rc.market_cfg.stocks)
        self.assertEqual(date(2020, 1, 1), rc.market_cfg.from_date)
        self.assertEqual(date(2021, 1, 1), rc.market_cfg.untill_date)
        self.assertEqual(2, len(rc.strategy_cfg.keys()))
        self.assertEqual(1, rc.strategy_cfg["p1"])
        self.assertEqual(2, rc.strategy_cfg["p2"])

    def test_WHEN_hash_or_equal_compare_THEN_compare_correctly(self):
        # Array
        si = StrategyId("test", "0.0.1")
        s1 = StockConfig("A", TimeFrame.D)
        s2 = StockConfig("B", TimeFrame.D)
        rc1 = RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                        date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))
        rc2 = RunConfig(StrategyId("test", "0.0.1"), MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                        date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))

        s3 = StockConfig("b", TimeFrame.D)
        wrong_rc_arr = [
            RunConfig(s1, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            RunConfig(s1, MarketConfig([s1, s2], TimeFrame.m1, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            RunConfig(si, MarketConfig([s1, s3], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 2),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 2)), StrategyConfig({"p1": 1, "p2": 2})),
            RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"P1": 1, "p2": 2})),
            RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 2, "p2": 2})),
            RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1})),
            RunConfig(si, MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2, "p3": 3})),
            RunConfig(si, MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            RunConfig(si, MarketConfig([s1, s2, s3], TimeFrame.D, date(2020, 1, 1),
                                       date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2})),
            RunConfig(StrategyId("test", "0.0.2"), MarketConfig([s1, s2], TimeFrame.D, date(2020, 1, 1),
                                                                date(2021, 1, 1)), StrategyConfig({"p1": 1, "p2": 2}))]
        # Act

        # Assert
        self.assertEqual(hash(rc1), hash(rc2))
        self.assertEqual(rc1, rc2)

        for wrong_rc in wrong_rc_arr:
            self.assertNotEqual(hash(rc1), hash(wrong_rc),
                                msg=wrong_rc)
            self.assertNotEqual(rc1, wrong_rc)

