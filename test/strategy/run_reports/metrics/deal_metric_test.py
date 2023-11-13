from __future__ import annotations
from math import sqrt
import unittest
import logging
from datetime import datetime
from src.strategy.run_report import Deal
from src.strategy.run_report.metrics.deal_metric import DealMetric


class DealMetric_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_no_deals_THEN_return_0(self):
        used_cap = {
            datetime(2023, 9, 1): 10.5,
            datetime(2023, 9, 3): 12.2,
            datetime(2023, 9, 2): 15.7,
        }
        asserted_rep = DealMetric([])

        # Act
        asserted_deal_count = asserted_rep.deal_count

        # Assert
        self.assertEqual(0, asserted_deal_count)

    def test_WHEN_request_deal_count_THEN_correct_return(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3),
            Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3),
            Deal(datetime(2023, 9, 2), 1, None, 2, 3)
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_deal_count = asserted_rep.deal_count

        # Assert
        self.assertEqual(3, asserted_deal_count)

    def test_WHEN_request_success_and_fail_deal_count_THEN_return_correct_info(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3),
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 2, 3),
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 3), 2, 3),
            Deal(datetime(2023, 9, 1), 2, None, 5, 3),
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_success_deal_count = asserted_rep.success_deal
        asserted_loss_deal_count = asserted_rep.fail_deal

        # Assert
        self.assertEqual(2, asserted_success_deal_count)
        self.assertEqual(1, asserted_loss_deal_count)

class DealMetric_avg_net_profit_income_loss_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                                datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_no_deal_THEN_0(self):
        # Array
        deals = [
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_net_profit
        asserted_avg_net_income = asserted_rep.avg_net_income
        asserted_avg_net_loss = asserted_rep.avg_net_loss

        # Assert
        self.assertIsNone(asserted_avg_net_profit)
        self.assertEqual(0, asserted_avg_net_income)
        self.assertEqual(0, asserted_avg_net_loss)

    def test_WHEN_pos_deals_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3),  #+3
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 6, 3),  #+6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3),  #0
            Deal(datetime(2023, 9, 1), 2, None, 4, 3),                  #+6
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_net_profit
        asserted_avg_net_income = asserted_rep.avg_net_income
        asserted_avg_net_loss = asserted_rep.avg_net_loss

        # Assert
        self.assertEqual(15/4, asserted_avg_net_profit)        
        self.assertEqual(5, asserted_avg_net_income)
        self.assertEqual(0, asserted_avg_net_loss)

    def test_WHEN_neg_deals_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 2), 1, 3),  #-3
            Deal(datetime(2023, 9, 2), 6, datetime(2023, 9, 3), 4, 3),  #-6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3),  #0
            Deal(datetime(2023, 9, 1), 4, None, 2, 3),                  #-6
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_net_profit
        asserted_avg_net_income = asserted_rep.avg_net_income
        asserted_avg_net_loss = asserted_rep.avg_net_loss

        # Assert
        self.assertEqual(-15/4, asserted_avg_net_profit)
        self.assertEqual(0, asserted_avg_net_income)
        self.assertEqual(-5, asserted_avg_net_loss)

    def test_WHEN_mixed_deals_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 2), 1, 3),  #-3
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 6, 3),  #+6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3),  #0
            Deal(datetime(2023, 9, 1), 2, None, 4, 3),                  #+6
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_net_profit
        asserted_avg_net_income = asserted_rep.avg_net_income
        asserted_avg_net_loss = asserted_rep.avg_net_loss

        # Assert
        self.assertEqual(9/4, asserted_avg_net_profit)
        self.assertEqual(6, asserted_avg_net_income)
        self.assertEqual(-3, asserted_avg_net_loss)

class DealMetric_PROM_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN__THEN_(self):
    # Array
        deals = [
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 2), 1, 3),  #-3
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 6, 3),  #+6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3),  #0
            Deal(datetime(2023, 9, 1), 2, None, 4, 3),                  #+6
        ]
        asserted_rep = DealMetric(deals)
        expected_AGP = 6 * (2 - sqrt(2))
        expected_AGL = -3 * (1 + sqrt(1))
        expected_M = 6 * 2 - 3 * 1
        expected_PROM = (expected_AGP + expected_AGL)/expected_M
        # Act
        asserted_PROM = asserted_rep.PROM

        # Assert
        self.assertAlmostEqual(expected_PROM, asserted_PROM,5)