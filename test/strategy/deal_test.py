import unittest
import logging
from src.strategy.deal import Deal, datetime


class Deal_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN__THEN_(self):
    # Array
    base_d = Deal(datetime(2020, 1, 1), 1, datetime(2020, 2, 1), 2, 1)
    eq_d_arr = [
        Deal(datetime(2020, 1, 1), 1, datetime(2020, 2, 1), 2, 1)
    ]
    not_eq_d_arr = [
        Deal(datetime(2020, 1, 1), 1, datetime(2020, 2, 2), 2, 1),
        Deal(datetime(2020, 1, 2), 1, datetime(2020, 2, 1), 2, 1),
        Deal(datetime(2020, 1, 1), 2, datetime(2020, 1, 1), 2, 1),
        Deal(datetime(2020, 1, 1), 1, datetime(2020, 1, 1), 3, 1),
        Deal(datetime(2020, 1, 1), 1, datetime(2020, 1, 1), 2, 2),
        Deal(datetime(2020, 1, 1), 1, datetime(
            2020, 1, 1), 2, 1, commission_open=-1),
        Deal(datetime(2020, 1, 1), 1, datetime(
            2020, 1, 1), 2, 1, commission_close=-1),
        Deal(datetime(2020, 1, 1), 1, datetime(
            2020, 1, 1), 2, 1, commission_holding=-1)
    ]
    # Act

    # Assert
    for d in eq_d_arr:
      self.assertEqual(hash(base_d), hash(d), msg=d)
      self.assertEqual(base_d, d, msg=d)

    for d in not_eq_d_arr:
      self.assertNotEqual(hash(base_d), hash(d), msg=d)
      self.assertNotEqual(base_d, d, msg=d)
