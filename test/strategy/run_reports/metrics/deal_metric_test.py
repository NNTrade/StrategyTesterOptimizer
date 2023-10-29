from __future__ import annotations
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
