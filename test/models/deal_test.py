import unittest
import logging
from src.models.deal import Deal, datetime


class Deal_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_long_deal_is_opened_THEN_properties_is_correct(self):
        # Array
        asserted_deal = Deal(datetime(2020, 1, 1), open_price=123,
                             amount=2, asset="A", capital=10, commission_open=-3)
        # Act

        # Assert
        self.assertEqual(asserted_deal.amount_abs, 2)
        self.assertEqual(asserted_deal.amount, 2)
        self.assertEqual(asserted_deal.open_price, 123)
        self.assertEqual(asserted_deal.asset, "A")
        self.assertEqual(asserted_deal.opened_capital, 10)
        self.assertFalse(asserted_deal.is_closed)
        self.assertEqual(asserted_deal.commission_open, -3)
        self.assertEqual(asserted_deal.commission_holding, 0)
        self.assertEqual(asserted_deal.commission_close, 0)
        self.assertEqual(asserted_deal.commission_total, -3)
        self.assertEqual(asserted_deal.opened_size, 123*2)
        self.assertEqual(asserted_deal.last_size, 123*2)

        self.assertTrue(asserted_deal.is_long)
        self.assertFalse(asserted_deal.is_short)
        self.assertEqual(asserted_deal.direction, "Long")
        self.assertEqual(asserted_deal.direction_mult, 1)

        self.assertEqual(asserted_deal.profit, -3)
        self.assertEqual(asserted_deal.interest_to_account, -3/10)
        self.assertEqual(asserted_deal.interest_to_position, -3/(123*2))

    def test_WHEN_short_deal_is_opened_THEN_properties_is_correct(self):
        # Array
        asserted_deal = Deal(datetime(2020, 1, 1), open_price=123,
                             amount=-2, asset="A", capital=10, commission_open=-3)
        # Act

        # Assert
        self.assertEqual(asserted_deal.open_date, datetime(2020, 1, 1))
        self.assertIsNone(asserted_deal.close_date)

        self.assertEqual(asserted_deal.amount_abs, 2)
        self.assertEqual(asserted_deal.amount, -2)

        self.assertEqual(asserted_deal.open_price, 123)
        self.assertEqual(asserted_deal.last_price, 123)
        self.assertIsNone(asserted_deal.close_price)

        self.assertEqual(asserted_deal.asset, "A")
        self.assertEqual(asserted_deal.opened_capital, 10)
        self.assertFalse(asserted_deal.is_closed)
        self.assertEqual(asserted_deal.commission_open, -3)
        self.assertEqual(asserted_deal.commission_holding, 0)
        self.assertEqual(asserted_deal.commission_close, 0)
        self.assertEqual(asserted_deal.commission_total, -3)

        self.assertEqual(asserted_deal.opened_size, 123*2)
        self.assertEqual(asserted_deal.last_size, 123*2)

        self.assertFalse(asserted_deal.is_long)
        self.assertTrue(asserted_deal.is_short)
        self.assertEqual(asserted_deal.direction, "Short")
        self.assertEqual(asserted_deal.direction_mult, -1)
        self.assertEqual(asserted_deal.profit, -3)
        self.assertEqual(asserted_deal.interest_to_account, -3/10)
        self.assertEqual(asserted_deal.interest_to_position, -3/(123*2))

    def test_WHEN_add_commission_THEN_commission_is_changed(self):
        # Array
        asserted_deal = Deal(datetime(2020, 1, 1), open_price=123,
                             amount=2, asset="A", capital=10, commission_open=-3)

        # Act
        asserted_deal.add_commision_holding(-5)
        # Assert
        self.assertEqual(asserted_deal.commission_open, -3)
        self.assertEqual(asserted_deal.commission_holding, -5)
        self.assertEqual(asserted_deal.commission_close, 0)
        self.assertEqual(asserted_deal.commission_total, -8)

        self.assertEqual(asserted_deal.profit, -8)
        self.assertEqual(asserted_deal.interest_to_account, -8/10)
        self.assertEqual(asserted_deal.interest_to_position, -8/(123*2))

        # Act
        asserted_deal.add_commision_holding(-2)
        # Assert
        self.assertEqual(asserted_deal.commission_open, -3)
        self.assertEqual(asserted_deal.commission_holding, -7)
        self.assertEqual(asserted_deal.commission_close, 0)
        self.assertEqual(asserted_deal.commission_total, -10)

        self.assertEqual(asserted_deal.profit, -10)
        self.assertEqual(asserted_deal.interest_to_account, -10/10)
        self.assertEqual(asserted_deal.interest_to_position, -10/(123*2))

    def test_WHEN_update_last_price_THEN_commission_is_changed(self):
        # Array
        asserted_deal = Deal(datetime(2020, 1, 1), open_price=123,
                             amount=2, asset="A", capital=10, commission_open=-3)

        # Act
        asserted_deal.set_last_price(130)

        # Assert
        self.assertEqual(asserted_deal.open_price, 123)
        self.assertEqual(asserted_deal.last_price, 130)
        self.assertIsNone(asserted_deal.close_price)

        self.assertEqual(asserted_deal.profit, 11)
        self.assertEqual(asserted_deal.interest_to_account, 11/10)
        self.assertEqual(asserted_deal.interest_to_position, 11/(123*2))

        self.assertEqual(asserted_deal.opened_size, 123*2)
        self.assertEqual(asserted_deal.last_size, 130*2)

        # Act
        asserted_deal.set_last_price(124)

        # Assert
        self.assertEqual(asserted_deal.open_price, 123)
        self.assertEqual(asserted_deal.last_price, 124)
        self.assertIsNone(asserted_deal.close_price)

        self.assertEqual(asserted_deal.profit, -1)
        self.assertEqual(asserted_deal.interest_to_account, -1/10)
        self.assertEqual(asserted_deal.interest_to_position, -1/(123*2))

        self.assertEqual(asserted_deal.opened_size, 123*2)
        self.assertEqual(asserted_deal.last_size, 124*2)

    def test_WHEN_long_deal_is_closed_with_gain_THEN_properties_is_correct(self):
        # Array
        asserted_deal = Deal(datetime(2020, 1, 1), open_price=123,
                             amount=2, asset="A", capital=10, commission_open=-3)

        # Act
        asserted_deal.add_commision_holding(-5)
        asserted_deal.close_deal(datetime(2020, 1, 3), 130, -4)

        # Assert
        self.assertEqual(asserted_deal.open_price, 123)
        self.assertEqual(asserted_deal.last_price, 130)
        self.assertEqual(asserted_deal.close_price, 130)

        self.assertTrue(asserted_deal.is_closed)
        self.assertEqual(asserted_deal.commission_close, -4)
        self.assertEqual(asserted_deal.commission_total, -12)
        self.assertEqual(asserted_deal.profit, 2)

        self.assertEqual(asserted_deal.interest_to_account, 2/10)
        self.assertEqual(asserted_deal.interest_to_position, 2/(123*2))

        self.assertEqual(asserted_deal.opened_size, 123*2)
        self.assertEqual(asserted_deal.last_size, 130*2)

    def test_WHEN_long_deal_is_closed_with_loss_THEN_properties_is_correct(self):
        # Array
        asserted_deal = Deal(datetime(2020, 1, 1), open_price=123,
                             amount=2, asset="A", capital=10, commission_open=-3)

        # Act
        asserted_deal.add_commision_holding(-5)
        asserted_deal.close_deal(datetime(2020, 1, 3), 120, -4)

        # Assert
        self.assertEqual(asserted_deal.open_price, 123)
        self.assertEqual(asserted_deal.last_price, 120)
        self.assertEqual(asserted_deal.close_price, 120)

        self.assertTrue(asserted_deal.is_closed)
        self.assertEqual(asserted_deal.commission_close, -4)
        self.assertEqual(asserted_deal.commission_total, -12)
        self.assertEqual(asserted_deal.profit, -18)

        self.assertEqual(asserted_deal.interest_to_account, -18/10)
        self.assertEqual(asserted_deal.interest_to_position, -18/(123*2))

        self.assertEqual(asserted_deal.opened_size, 123*2)
        self.assertEqual(asserted_deal.last_size, 120*2)

    def test_WHEN_short_deal_is_closed_with_gain_THEN_properties_is_correct(self):
        # Array
        asserted_deal = Deal(datetime(2020, 1, 1), open_price=123,
                             amount=-2, asset="A", capital=10, commission_open=-3)

        # Act
        asserted_deal.add_commision_holding(-5)
        asserted_deal.close_deal(datetime(2020, 1, 3), 110, -4)

        # Assert
        self.assertEqual(asserted_deal.open_price, 123)
        self.assertEqual(asserted_deal.last_price, 110)
        self.assertEqual(asserted_deal.close_price, 110)

        self.assertTrue(asserted_deal.is_closed)
        self.assertEqual(asserted_deal.commission_close, -4)
        self.assertEqual(asserted_deal.commission_total, -12)
        self.assertEqual(asserted_deal.profit, 14)

        self.assertEqual(asserted_deal.interest_to_account, 14/10)
        self.assertEqual(asserted_deal.interest_to_position, 14/(123*2))

        self.assertEqual(asserted_deal.opened_size, 123*2)
        self.assertEqual(asserted_deal.last_size, 110*2)

    def test_WHEN_short_deal_is_closed_with_loss_THEN_properties_is_correct(self):
        # Array
        asserted_deal = Deal(datetime(2020, 1, 1), open_price=123,
                             amount=-2, asset="A", capital=10, commission_open=-3)

        # Act
        asserted_deal.add_commision_holding(-5)
        asserted_deal.close_deal(datetime(2020, 1, 3), 126, -4)

        # Assert
        self.assertEqual(asserted_deal.open_price, 123)
        self.assertEqual(asserted_deal.last_price, 126)
        self.assertEqual(asserted_deal.close_price, 126)

        self.assertTrue(asserted_deal.is_closed)
        self.assertEqual(asserted_deal.commission_close, -4)
        self.assertEqual(asserted_deal.commission_total, -12)
        self.assertEqual(asserted_deal.profit, -18)

        self.assertEqual(asserted_deal.interest_to_account, -18/10)
        self.assertEqual(asserted_deal.interest_to_position, -18/(123*2))

        self.assertEqual(asserted_deal.opened_size, 123*2)
        self.assertEqual(asserted_deal.last_size, 126*2)

    def test_WHEN_compare_THEN_correct_result(self):
        # Array
        base_d = Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -1)
        eq_d_arr = [
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -1)
        ]
        not_eq_d_arr = [
            Deal(datetime(2020, 1, 1), 10, 100, "A",
                 0.3, -1).add_commision_holding(3),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -
                 1).close_deal(datetime(2020, 1, 2), 3),
            Deal(datetime(2020, 1, 2), 10, 100, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 11, 100, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 101, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "B", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.4, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -3),
        ]
        # Act

        # Assert
        print(base_d)

        for d in eq_d_arr:
            self.assertEqual(hash(base_d), hash(d), msg=d)
            self.assertEqual(base_d, d, msg=d)

        for d in not_eq_d_arr:
            self.assertNotEqual(hash(base_d), hash(d), msg=d)
            self.assertNotEqual(base_d, d, msg=d)

    def test_WHEN_compare_commision_closed_THEN_correct_result(self):
        # Array
        base_d = Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -
                      1).set_last_price(14).close_deal(datetime(2020, 1, 3), 18)
        eq_d_arr = [
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -
                 1).set_last_price(14).close_deal(datetime(2020, 1, 3), 18)
        ]
        not_eq_d_arr = [
            Deal(datetime(2020, 1, 1), 10, 100, "A",
                 0.3, -1).add_commision_holding(3),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -
                 1).close_deal(datetime(2020, 1, 2), 3),
            Deal(datetime(2020, 1, 2), 10, 100, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 11, 100, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 101, "A", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "B", 0.3, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.4, -1),
            Deal(datetime(2020, 1, 1), 10, 100, "A", 0.3, -3),
        ]
        # Act

        # Assert
        print(base_d)

        for d in eq_d_arr:
            self.assertEqual(hash(base_d), hash(d), msg=d)
            self.assertEqual(base_d, d, msg=d)

        for d in not_eq_d_arr:
            self.assertNotEqual(hash(base_d), hash(d), msg=d)
            self.assertNotEqual(base_d, d, msg=d)

    def test_WHEN_serialization_and_deserialization_THEN_equals(self):
        # Array
        expected_cfg = Deal(datetime(2020, 1, 2, 10, 12, 3),
                            1.2, 10, "A", 0.2, -1.2)

        # Act
        json_str = expected_cfg.to_json()

        # Parse the JSON back into a DTO
        asserted_cfg = Deal.from_json(json_str)

        # Assert
        self.assertEqual(expected_cfg, asserted_cfg)

    def test_WHEN_open_with_commision_serialization_and_deserialization_THEN_equals(self):
        # Array
        expected_cfg = Deal(datetime(2020, 1, 2, 10, 12, 3),
                            1.2, 10, "A", 0.2, -1.2)
        expected_cfg.add_commision_holding(10)

        # Act
        json_str = expected_cfg.to_json()

        # Parse the JSON back into a DTO
        asserted_cfg = Deal.from_json(json_str)

        # Assert
        self.assertEqual(expected_cfg, asserted_cfg)

    def test_WHEN_closed_serialization_and_deserialization_THEN_equals(self):
        # Array
        expected_cfg = Deal(datetime(2020, 1, 2, 10, 12, 3),
                            1.2, 10, "A", 0.2, -1.2)
        expected_cfg.add_commision_holding(10)
        expected_cfg.close_deal(datetime(2020, 1, 3, 10, 12, 3), 2, -0.8)

        # Act
        json_str = expected_cfg.to_json()

        # Parse the JSON back into a DTO
        asserted_cfg = Deal.from_json(json_str)

        # Assert
        self.assertEqual(expected_cfg, asserted_cfg)
