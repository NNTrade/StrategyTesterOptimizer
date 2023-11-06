from __future__ import annotations
import unittest
import logging
from datetime import datetime
from src.strategy.run_report.metrics.capital_metric import CapitalMetric
from src.strategy.run_config import MarketConfig, StockConfig, TimeFrame,date

class CapitalMetric_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_empty_cap_THEN_exception(self):
        # Array

        # Act

        # Assert
        with self.assertRaises(AttributeError) as context:
            CapitalMetric(None,{})

    def test_WHEN_request_str_yield_THEN_correct_return(self):
        # Array
        s1 = StockConfig("S1", TimeFrame.D)
        s2 = StockConfig("S2", TimeFrame.D)
        mc = MarketConfig([s1, s2], TimeFrame.D, date(
            2021, 9, 1), date(2023, 9, 1))
        used_cap = {
            datetime(2021, 9, 1): 100,
            datetime(2023, 8, 30): 121,
            datetime(2021, 9, 2): 15.7,
        }
        asserted_rep = CapitalMetric(mc, used_cap)

        # Act
        asserted_net_cap = asserted_rep.strategy_yield_per_year

        # Assert
        self.assertEqual(2* 365, mc.period_in_days)
        self.assertEqual(2, mc.period_in_years)
        self.assertAlmostEquals(0.1, asserted_net_cap, 5)

    def test_WHEN_request_str_yield_per_year_THEN_correct_return(self):
        # Array
        used_cap = {
            datetime(2023, 9, 1): 10.5,
            datetime(2024, 9, 3): 12.2,
            datetime(2023, 9, 2): 15.7,
        }
        asserted_rep = CapitalMetric(None,used_cap)

        # Act
        asserted_net_cap = asserted_rep.strategy_yield

        # Assert
        self.assertEqual(12.2/10.5 - 1, asserted_net_cap)

    def test_WHEN_request_max_str_yield_THEN_correct_return(self):
        # Array
        used_cap = {
            datetime(2023, 9, 1): 10.5,
            datetime(2023, 9, 3): 12.2,
            datetime(2023, 9, 2): 15.7,
        }
        asserted_rep = CapitalMetric(None,used_cap)

        # Act
        asserted_net_cap = asserted_rep.strategy_max_yield

        # Assert
        self.assertEqual(15.7/10.5 - 1, asserted_net_cap)

    def assert_max_fall(self, used_list, expect_value):
        # Array
        used_cap = {}
        for i, v in enumerate(used_list):
            used_cap[datetime(2023, 9, i+1)] = v

        asserted_rep = CapitalMetric(None,used_cap)
        # Act
        asserted_max_fall = asserted_rep.max_fall

        # Assert
        self.assertEqual(expect_value, asserted_max_fall)

    def test_WHEN_single_element_THEN_correct_return(self):
        self.assert_max_fall([10], 0)

    def test_WHEN_no_falls_THEN_correct_return(self):
        self.assert_max_fall([10, 20, 30, 40], 0)

    def test_WHEN_positive_fall_THEN_correct_return(self):
        self.assert_max_fall([50, 40, 30, 20, 10], -40/50)

    def test_WHEN_negative_fall_THEN_correct_return(self):
        self.assert_max_fall([10, 20, 5, 30, 15], -15/20)

    def test_WHEN_multiple_falls_THEN_correct_return(self):
        self.assert_max_fall([50, 40, 60, 30, 20, 10, 70, 5], -65/70)
