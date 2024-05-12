from __future__ import annotations
from math import sqrt
from typing import List
import unittest
import logging
from datetime import datetime
from src.simulation.models import Deal
from src.metrics import DealMetric


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
            Deal(datetime(2023, 9, 1), 1, 3, "A", 10),
            Deal(datetime(2023, 9, 2), 1, 3, "A", 10),
            Deal(datetime(2023, 9, 2), 1, 3, "A", 10)
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_deal_count = asserted_rep.deal_count

        # Assert
        self.assertEqual(3, asserted_deal_count)

    def test_WHEN_request_success_and_fail_deal_count_THEN_return_correct_info(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), 1, 3, "A", 10).close_deal(
                datetime(2023, 9, 2), 2),
            Deal(datetime(2023, 9, 2), 4, 4, "A", 10).close_deal(
                datetime(2023, 9, 3), 2),
            Deal(datetime(2023, 9, 1), 2, 2, "A", 10).close_deal(
                datetime(2023, 9, 3), 3),
            Deal(datetime(2023, 9, 1), 2, 5, "A", 10),
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_success_deal_count = asserted_rep.success_deal
        asserted_loss_deal_count = asserted_rep.fail_deal

        # Assert
        self.assertEqual(2, asserted_success_deal_count)
        self.assertEqual(1, asserted_loss_deal_count)


class DealMetric_avg_net_profit_by_all_success_loss_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_no_deal_THEN_0(self):
        # Array
        deals = [
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_profit_all
        asserted_avg_net_income = asserted_rep.avg_profit_by_success
        asserted_avg_net_loss = asserted_rep.avg_profit_by_loss

        # Assert
        self.assertIsNone(asserted_avg_net_profit)
        self.assertEqual(0, asserted_avg_net_income)
        self.assertEqual(0, asserted_avg_net_loss)

    def test_WHEN_pos_deals_THEN_correct(self):
        # Array
        deals: List[Deal] = [
            # +3/6
            Deal(datetime(2023, 9, 1), open_price=1, asset="A", amount=1,
                 capital=6).close_deal(datetime(2023, 9, 2), 4),  # +3/6
            Deal(datetime(2023, 9, 2), open_price=4, asset="A", amount=3,
                 capital=6).close_deal(datetime(2023, 9, 3), 6),  # +6/6
            Deal(datetime(2023, 9, 2), open_price=3, asset="A", amount=3,
                 # 0
                 capital=10).close_deal(date=datetime(2023, 9, 3), price=3),
            Deal(datetime(2023, 9, 1), open_price=2, asset="A",
                 amount=3, capital=12).set_last_price(datetime(2023, 9, 4),4),  # +6/12
        ]
        assert deals[0].profit == 3
        assert deals[1].profit == 6
        assert deals[2].profit == 0
        assert deals[3].profit == 6

        asserted_rep = DealMetric(deals)
        # Act
        asserted_avg_net_profit = asserted_rep.avg_profit_all
        asserted_avg_net_income = asserted_rep.avg_profit_by_success
        asserted_avg_net_loss = asserted_rep.avg_profit_by_loss

        # Assert
        self.assertAlmostEqual(
            (3+6+6)/4, asserted_avg_net_profit)  # type: ignore
        self.assertAlmostEqual((3+6+6)/3, asserted_avg_net_income)
        self.assertAlmostEqual(0, asserted_avg_net_loss)

    def test_WHEN_neg_deals_THEN_correct(self):
        # Array
        deals: List[Deal] = [
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, capital=6,
                 asset="A").close_deal(datetime(2023, 9, 2), 1),  # -3/6
            Deal(datetime(2023, 9, 2), open_price=6, amount=3, capital=6,
                 asset="A").close_deal(datetime(2023, 9, 3), 4),  # -6/6
            Deal(datetime(2023, 9, 2), open_price=3, amount=3, capital=10,
                 asset="A").close_deal(datetime(2023, 9, 3), 3),  # 0
            Deal(datetime(2023, 9, 1), open_price=4, amount=3,
                 capital=12, asset="A").set_last_price(datetime(2023, 9, 4),2),  # -6/12
        ]
        assert deals[0].profit == -3
        assert deals[1].profit == -6
        assert deals[2].profit == 0
        assert deals[3].profit == -6

        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_profit_all
        asserted_avg_net_income = asserted_rep.avg_profit_by_success
        asserted_avg_net_loss = asserted_rep.avg_profit_by_loss

        # Assert
        self.assertAlmostEqual(
            (-3-6-6)/4, asserted_avg_net_profit)  # type: ignore
        self.assertAlmostEqual(0, asserted_avg_net_income)
        self.assertAlmostEqual((-3-6-6)/3, asserted_avg_net_loss)

    def test_WHEN_mixed_deals_THEN_correct(self):
        # Array
        deals: List[Deal] = [
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 2), 1),  # -3
            Deal(datetime(2023, 9, 2), open_price=4, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 6),  # +6
            Deal(datetime(2023, 9, 2), open_price=3, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 3),  # 0
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, asset="A",
                 capital=10).set_last_price(datetime(2023, 9, 4),4),  # +6
        ]
        assert deals[0].profit == -3
        assert deals[1].profit == 6
        assert deals[2].profit == 0
        assert deals[3].profit == 6
        asserted_rep = DealMetric(deals)

        # Act
        asserted_avg_net_profit = asserted_rep.avg_profit_all
        asserted_avg_net_income = asserted_rep.avg_profit_by_success
        asserted_avg_net_loss = asserted_rep.avg_profit_by_loss

        # Assert
        self.assertAlmostEqual(
            (6+6-3)/4, asserted_avg_net_profit)  # type: ignore
        self.assertAlmostEqual(6, asserted_avg_net_income)  # type: ignore
        self.assertAlmostEqual(-3, asserted_avg_net_loss)  # type: ignore


class DealMetric_avg_net_interest_by_all_success_loss_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_no_deal_THEN_0(self):
        # Array
        deals = [
        ]
        asserted_rep = DealMetric(deals)

        # Act

        # Assert
        self.assertIsNone(asserted_rep.avg_interest_to_position_all)
        self.assertEqual(0, asserted_rep.avg_interest_to_account_by_success)
        self.assertEqual(0, asserted_rep.avg_interest_to_account_by_loss)

        self.assertIsNone(asserted_rep.avg_interest_to_position_all)
        self.assertEqual(0, asserted_rep.avg_interest_to_account_by_success)
        self.assertEqual(0, asserted_rep.avg_interest_to_account_by_loss)

    def test_WHEN_pos_deals_THEN_correct(self):
        # Array
        deals: List[Deal] = [
            # +3/6
            Deal(datetime(2023, 9, 1), open_price=1, asset="A", amount=1,
                 capital=6).close_deal(datetime(2023, 9, 2), 4),  # +3/6
            Deal(datetime(2023, 9, 2), open_price=4, asset="A", amount=3,
                 capital=6).close_deal(datetime(2023, 9, 3), 6),  # +6/6
            Deal(datetime(2023, 9, 2), open_price=3, asset="A", amount=3,
                 # 0
                 capital=10).close_deal(date=datetime(2023, 9, 3), price=3),
            Deal(datetime(2023, 9, 1), open_price=2, asset="A",
                 amount=3, capital=12).set_last_price(datetime(2023, 9, 4),4),  # +6/12
        ]
        assert deals[0].interest_to_account == 3/6
        assert deals[1].interest_to_account == 6/6
        assert deals[2].interest_to_account == 0/6
        assert deals[3].interest_to_account == 6/12

        assert deals[0].interest_to_position == 3/(1*1)
        assert deals[1].interest_to_position == 6/(4*3)
        assert deals[2].interest_to_position == 0/(3*3)
        assert deals[3].interest_to_position == 6/(2*3)

        asserted_rep = DealMetric(deals)
        # Act

        # Assert
        self.assertAlmostEqual(
            (3/6+6/6+6/12)/4, asserted_rep.avg_interest_to_account_all)  # type: ignore
        self.assertAlmostEqual(
            (3/6+6/6+6/12)/3, asserted_rep.avg_interest_to_account_by_success)
        self.assertAlmostEqual(0, asserted_rep.avg_interest_to_account_by_loss)

        self.assertAlmostEqual(
            (3/1+6/12+6/6)/4, asserted_rep.avg_interest_to_position_all)  # type: ignore
        self.assertAlmostEqual(
            (3/1+6/12+6/6)/3, asserted_rep.avg_interest_to_position_by_success)
        self.assertAlmostEqual(
            0, asserted_rep.avg_interest_to_position_by_loss)

    def test_WHEN_neg_deals_THEN_correct(self):
        # Array
        deals: List[Deal] = [
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, capital=6,
                 asset="A").close_deal(datetime(2023, 9, 2), 1),  # -3/6
            Deal(datetime(2023, 9, 2), open_price=6, amount=3, capital=6,
                 asset="A").close_deal(datetime(2023, 9, 3), 4),  # -6/6
            Deal(datetime(2023, 9, 2), open_price=3, amount=3, capital=10,
                 asset="A").close_deal(datetime(2023, 9, 3), 3),  # 0
            Deal(datetime(2023, 9, 1), open_price=4, amount=3,
                 capital=12, asset="A").set_last_price(datetime(2023, 9, 4),2),  # -6/12
        ]
        assert deals[0].interest_to_account == -3/6
        assert deals[1].interest_to_account == -6/6
        assert deals[2].interest_to_account == 0
        assert deals[3].interest_to_account == -6/12

        assert deals[0].interest_to_position == -3/(2*3)
        assert deals[1].interest_to_position == -6/(6*3)
        assert deals[2].interest_to_position == 0/(3*3)
        assert deals[3].interest_to_position == -6/(4*3)
        asserted_rep = DealMetric(deals)

        # Act

        # Assert
        self.assertAlmostEqual(
            (-0.5-1-0.5)/4, asserted_rep.avg_interest_to_account_all)  # type: ignore
        self.assertAlmostEqual(
            0, asserted_rep.avg_interest_to_account_by_success)
        self.assertAlmostEqual(
            (-0.5-1-0.5)/3,  asserted_rep.avg_interest_to_account_by_loss)
        
        self.assertAlmostEqual(
            (-3/(2*3)-6/(6*3)-6/(4*3))/4, asserted_rep.avg_interest_to_position_all)  # type: ignore
        self.assertAlmostEqual(
            0, asserted_rep.avg_interest_to_position_by_success)
        self.assertAlmostEqual(
            (-3/(2*3)-6/(6*3)-6/(4*3))/3,  asserted_rep.avg_interest_to_position_by_loss)

    def test_WHEN_mixed_deals_THEN_correct(self):
        # Array
        deals: List[Deal] = [
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 2), 1),  # -3/10
            Deal(datetime(2023, 9, 2), open_price=4, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 6),  # +6/10
            Deal(datetime(2023, 9, 2), open_price=3, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 3),  # 0/10
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, asset="A",
                 capital=10).set_last_price(datetime(2023, 9, 4),4),  # +6/10
        ]
        assert deals[0].interest_to_account == -3/10
        assert deals[1].interest_to_account == 6/10
        assert deals[2].interest_to_account == 0
        assert deals[3].interest_to_account == 6/10

        assert deals[0].interest_to_position == -3/(2*3)
        assert deals[1].interest_to_position == 6/(4*3)
        assert deals[2].interest_to_position == 0
        assert deals[3].interest_to_position == 6/(2*3)

        asserted_rep = DealMetric(deals)

        # Act

        # Assert
        self.assertAlmostEqual(
            (-3/10+6/10+6/10)/4, asserted_rep.avg_interest_to_account_all)  # type: ignore
        self.assertAlmostEqual(
            (6/10+6/10)/2, asserted_rep.avg_interest_to_account_by_success)  # type: ignore
        self.assertAlmostEqual(
            (-3/10)/1, asserted_rep.avg_interest_to_account_by_loss)  # type: ignore
        
        self.assertAlmostEqual(
            (-3/(2*3)+6/(4*3)+6/(2*3))/4, asserted_rep.avg_interest_to_position_all)  # type: ignore
        self.assertAlmostEqual(
            (6/(4*3)+6/(2*3))/2, asserted_rep.avg_interest_to_position_by_success)  # type: ignore
        self.assertAlmostEqual(
            (-3/(2*3))/1, asserted_rep.avg_interest_to_position_by_loss)  # type: ignore


class DealMetric_PROM_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_request_THEN_correct(self):
        # Array
        deals: List[Deal] = [
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 2), 1),  # -3
            Deal(datetime(2023, 9, 2), open_price=4, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 6),  # +6
            Deal(datetime(2023, 9, 2), open_price=3, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 3),  # 0
            Deal(datetime(2023, 9, 1), open_price=2, amount=3,
                 asset="A", capital=10).set_last_price(datetime(2023, 9, 4),4),  # +6
        ]
        assert deals[0].profit == -3
        assert deals[1].profit == 6
        assert deals[2].profit == 0
        assert deals[3].profit == 6

        asserted_rep = DealMetric(deals)
        expected_AGP = 6/10 * (2 - sqrt(2))
        expected_AGL = -3/10 * (1 + sqrt(1))
        expected_M = 6/10 * 2 - 3/10 * 1
        expected_PROM = (expected_AGP + expected_AGL)/expected_M
        # Act
        asserted_PROM = asserted_rep.PROM

        # Assert
        self.assertIsNotNone(asserted_PROM)
        self.assertAlmostEqual(expected_PROM, asserted_PROM)  # type: ignore

    def test_WHEN_only_success_THEN_correct(self):
        # Array
        deals: List[Deal] = [
            Deal(datetime(2023, 9, 1), open_price=1, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 2), 2),  # +3
            Deal(datetime(2023, 9, 2), open_price=4, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 6),  # +6
            Deal(datetime(2023, 9, 2), open_price=3, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 3),  # 0
            Deal(datetime(2023, 9, 1), open_price=2,  amount=3,
                 asset="A", capital=10).set_last_price(datetime(2023, 9, 4),4),  # +6
        ]
        assert deals[0].profit == 3
        assert deals[1].profit == 6
        assert deals[2].profit == 0
        assert deals[3].profit == 6

        asserted_rep = DealMetric(deals)
        expected_AGP = 5/10 * (3 - sqrt(3))
        expected_AGL = 0 * (0 + sqrt(0))
        expected_M = 5/10 * 3 - 0 * 0
        expected_PROM = (expected_AGP + expected_AGL)/expected_M
        # Act
        asserted_PROM = asserted_rep.PROM

        # Assert
        self.assertIsNotNone(asserted_PROM)
        self.assertAlmostEqual(expected_PROM, asserted_PROM)  # type: ignore

    def test_WHEN_only_fail_THEN_correct(self):
        # Array
        deals = [
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 2), 1),  # -3
            Deal(datetime(2023, 9, 2), open_price=6, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 4),  # -6
            Deal(datetime(2023, 9, 2), open_price=3, amount=3, asset="A",
                 capital=10).close_deal(datetime(2023, 9, 3), 3),  # 0
            Deal(datetime(2023, 9, 1), open_price=4, amount=3, asset="A",
                 capital=10).set_last_price(datetime(2023, 9, 4),2),  # -6
        ]
        asserted_rep = DealMetric(deals)
        expected_AGP = 0
        expected_AGL = - 5/10 * (3 + sqrt(3))
        expected_M = -5/10 * 3
        expected_PROM = (expected_AGP + expected_AGL)/expected_M

        # Act
        asserted_PROM = asserted_rep.PROM

        # Assert
        self.assertIsNotNone(asserted_PROM)
        self.assertAlmostEqual(expected_PROM, asserted_PROM)  # type: ignore

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
            Deal(datetime(2023, 9, 2), open_price=3,  amount=3, capital=10,
                 asset="A").close_deal(datetime(2023, 9, 3), 3),  # 0
            Deal(datetime(2023, 9, 1), open_price=2, amount=3, capital=10,
                 asset="A").set_last_price(datetime(2023, 9, 4),2),  # 0
        ]
        asserted_rep = DealMetric(deals)

        # Act
        asserted_PROM = asserted_rep.PROM

        # Assert
        self.assertIsNone(asserted_PROM)
