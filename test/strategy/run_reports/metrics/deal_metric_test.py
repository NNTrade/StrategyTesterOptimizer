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
            Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,10),
            Deal(datetime(2023, 9, 2), 1, datetime(2023, 9, 3), 2, 3,10),
            Deal(datetime(2023, 9, 2), 1, None, 2, 3,10)
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_deal_count = asserted_rep.deal_count

        # Assert
        self.assertEqual(3, asserted_deal_count)

    def test_WHEN_request_success_and_fail_deal_count_THEN_return_correct_info(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,10),
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 2, 3,10),
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 3), 2, 3,10),
            Deal(datetime(2023, 9, 1), 2, None, 5, 3,10),
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
            Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,6),   #+3/6
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 6, 3,6),   #+6/6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3,10),  #0
            Deal(datetime(2023, 9, 1), 2, None, 4, 3,12),                  #+6/12
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_net_profit
        asserted_avg_net_income = asserted_rep.avg_net_income
        asserted_avg_net_loss = asserted_rep.avg_net_loss

        # Assert
        self.assertAlmostEqual(2/4, asserted_avg_net_profit,5)        
        self.assertAlmostEqual(2/3, asserted_avg_net_income,5)
        self.assertAlmostEqual(0, asserted_avg_net_loss,5)

    def test_WHEN_neg_deals_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 2), 1, 3,6),  #-3/6
            Deal(datetime(2023, 9, 2), 6, datetime(2023, 9, 3), 4, 3,6),  #-6/6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3,10),  #0
            Deal(datetime(2023, 9, 1), 4, None, 2, 3,12),                  #-6/12
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_net_profit
        asserted_avg_net_income = asserted_rep.avg_net_income
        asserted_avg_net_loss = asserted_rep.avg_net_loss

        # Assert
        self.assertAlmostEqual(-2/4, asserted_avg_net_profit,5)
        self.assertAlmostEqual(0, asserted_avg_net_income,5)
        self.assertAlmostEqual(-2/3, asserted_avg_net_loss,5)

    def test_WHEN_mixed_deals_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 2), 1, 3,10),  #-3
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 6, 3,10),  #+6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3,10),  #0
            Deal(datetime(2023, 9, 1), 2, None, 4, 3,10),                  #+6
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_net_profit
        asserted_avg_net_income = asserted_rep.avg_net_income
        asserted_avg_net_loss = asserted_rep.avg_net_loss

        # Assert
        self.assertAlmostEqual(9/4/10, asserted_avg_net_profit, 5)
        self.assertAlmostEqual(6/10, asserted_avg_net_income,5)
        self.assertAlmostEqual(-3/10, asserted_avg_net_loss,5)

class DealMetric_PROM_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_request_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 2), 1, 3,10),  #-3
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 6, 3,10),  #+6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3,10),  #0
            Deal(datetime(2023, 9, 1), 2, None, 4, 3,10),                  #+6
        ]
        asserted_rep = DealMetric(deals)
        expected_AGP = 6/10 * (2 - sqrt(2))
        expected_AGL = -3/10 * (1 + sqrt(1))
        expected_M = 6/10 * 2 - 3/10 * 1
        expected_PROM = (expected_AGP + expected_AGL)/expected_M
        # Act
        asserted_PROM = asserted_rep.PROM

        # Assert
        self.assertIsNotNone(asserted_PROM)
        self.assertAlmostEqual(expected_PROM, asserted_PROM,5)

    def test_WHEN_only_success_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 1, datetime(2023, 9, 2), 2, 3,10),  #+3
            Deal(datetime(2023, 9, 2), 4, datetime(2023, 9, 3), 6, 3,10),  #+6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3,10),  #0
            Deal(datetime(2023, 9, 1), 2, None, 4, 3,10),                  #+6
        ]
        asserted_rep = DealMetric(deals)
        expected_AGP = 5/10 * (3 - sqrt(3))
        expected_AGL = 0 * (0 + sqrt(0))
        expected_M = 5/10* 3 - 0 * 0
        expected_PROM = (expected_AGP + expected_AGL)/expected_M
        # Act
        asserted_PROM = asserted_rep.PROM

        # Assert
        self.assertIsNotNone(asserted_PROM)
        self.assertAlmostEqual(expected_PROM, asserted_PROM,5)

    def test_WHEN_only_fail_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 2, datetime(2023, 9, 2), 1, 3,10),  #-3
            Deal(datetime(2023, 9, 2), 6, datetime(2023, 9, 3), 4, 3,10),  #-6
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3,10),  #0
            Deal(datetime(2023, 9, 1), 4, None, 2, 3,10),                  #-6
        ]
        asserted_rep = DealMetric(deals)
        expected_AGP = 0
        expected_AGL = - 5/10 * (3 + sqrt(3))
        expected_M = -5/10* 3
        expected_PROM = (expected_AGP + expected_AGL)/expected_M

        # Act
        asserted_PROM = asserted_rep.PROM

        # Assert
        self.assertIsNotNone(asserted_PROM)
        self.assertAlmostEqual(expected_PROM, asserted_PROM,5)

    def test_WHEN_no_deal_THEN_None(self):
        # Array
        deals = []
        asserted_rep = DealMetric(deals)

        # Act
        asserted_PROM = asserted_rep.PROM
        
        # Assert
        self.assertIsNone(asserted_PROM)

    def test_WHEN_all_deals_is_zero_THEN_None(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 2), 3, datetime(2023, 9, 3), 3, 3,10),  #0
            Deal(datetime(2023, 9, 1), 2, None, 2, 3,10),                  #0
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_PROM = asserted_rep.PROM
        
        # Assert
        self.assertIsNone(asserted_PROM)