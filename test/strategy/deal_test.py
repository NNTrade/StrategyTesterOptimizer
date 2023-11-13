import unittest
import logging
from src.strategy.deal import Deal, datetime


class Deal_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN__THEN_(self):
        # Array
        base_d = Deal(datetime(2020, 1, 1), 1, datetime(2020, 2, 1), 2, 1, 3)
        eq_d_arr = [
            Deal(datetime(2020, 1, 1), 1, datetime(2020, 2, 1), 2, 1,3)
        ]
        not_eq_d_arr = [
            Deal(datetime(2020, 1, 1), 1, datetime(2020, 2, 1), 2, 1,2),
            Deal(datetime(2020, 1, 1), 1, datetime(2020, 2, 2), 2, 1,3),
            Deal(datetime(2020, 1, 2), 1, datetime(2020, 2, 1), 2, 1,3),
            Deal(datetime(2020, 1, 1), 2, datetime(2020, 1, 1), 2, 1,3),
            Deal(datetime(2020, 1, 1), 1, datetime(2020, 1, 1), 3, 1,3),
            Deal(datetime(2020, 1, 1), 1, datetime(2020, 1, 1), 2, 2,3),
            Deal(datetime(2020, 1, 1), 1, datetime(
                2020, 1, 1), 2, 1,3, commission_open=-1),
            Deal(datetime(2020, 1, 1), 1, datetime(
                2020, 1, 1), 2, 1,3, commission_close=-1),
            Deal(datetime(2020, 1, 1), 1, datetime(
                2020, 1, 1), 2, 1,3, commission_holding=-1)
        ]
        # Act

        # Assert
        for d in eq_d_arr:
            self.assertEqual(hash(base_d), hash(d), msg=d)
            self.assertEqual(base_d, d, msg=d)

        for d in not_eq_d_arr:
            self.assertNotEqual(hash(base_d), hash(d), msg=d)
            self.assertNotEqual(base_d, d, msg=d)

    def test_WHEN_request_result_or_profit_THEN_correct(self):
        # Array
        used_d = Deal(datetime(2020, 1, 1), 1, datetime(2020, 2, 1), 3, 2, 10)
       
        # Act
        asserted_result = used_d.result
        asserted_profit = used_d.profit

        # Assert    
        self.assertEqual(4, asserted_result)
        self.assertEqual(0.4, asserted_profit)

class DealBuilder_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_create_using_builder_THEN_correct(self):
        # Array
        db = Deal.Builder()
        expected_open_dt = datetime(2020, 1, 1)
        expected_open_pr = 1
        expected_close_dt = datetime(2020, 2, 2)
        expected_close_pr = 2
        expected_amount = 3
        expected_start_capital = 10
        expected_open_comm = -4
        expected_mid_comm = -5
        expected_close_comm = -6
        # Act
        db.set_open_date(expected_open_dt).set_open_price(expected_open_pr)\
          .set_close_date(expected_close_dt).set_close_price(expected_close_pr)\
          .set_amount(expected_amount)\
          .set_start_capital(expected_start_capital)\
          .set_commission_open(expected_open_comm)\
          .set_commission_holding(expected_mid_comm)\
          .set_commission_close(expected_close_comm)

        asserted_d = db.build()
        # Assert
        self.assertEqual(expected_open_dt, asserted_d.open_date)
        self.assertEqual(expected_open_pr, asserted_d.open_price)
        self.assertEqual(expected_close_dt, asserted_d.close_date)
        self.assertEqual(expected_close_pr, asserted_d.close_price)
        self.assertEqual(expected_amount, asserted_d.amount)
        self.assertEqual(expected_start_capital, asserted_d.start_capital)
        self.assertEqual(expected_open_comm, asserted_d.commission_open)
        self.assertEqual(expected_mid_comm, asserted_d.commission_holding)
        self.assertEqual(expected_close_comm, asserted_d.commission_close)

    def test_WHEN_create_no_closed_deal_THEN_correct(self):
        # Array
        db = Deal.Builder()
        expected_open_dt = datetime(2020, 1, 1)
        expected_open_pr = 1
        expected_close_dt = None
        expected_close_pr = 2
        expected_amount = 3
        expected_start_capital = 10
        expected_open_comm = -4
        expected_mid_comm = -5
        expected_close_comm = -6
        # Act
        db.set_open_date(expected_open_dt).set_open_price(expected_open_pr)\
          .set_close_date(expected_close_dt).set_close_price(expected_close_pr)\
          .set_amount(expected_amount)\
          .set_start_capital(expected_start_capital)\
          .set_commission_open(expected_open_comm)\
          .set_commission_holding(expected_mid_comm)\
          .set_commission_close(expected_close_comm)

        asserted_d = db.build()
        # Assert
        self.assertEqual(expected_open_dt, asserted_d.open_date)
        self.assertEqual(expected_open_pr, asserted_d.open_price)
        self.assertIsNone(asserted_d.close_date)
        self.assertEqual(expected_close_pr, asserted_d.close_price)
        self.assertEqual(expected_amount, asserted_d.amount)
        self.assertEqual(expected_start_capital, asserted_d.start_capital)
        self.assertEqual(expected_open_comm, asserted_d.commission_open)
        self.assertEqual(expected_mid_comm, asserted_d.commission_holding)
        self.assertEqual(expected_close_comm, asserted_d.commission_close)
