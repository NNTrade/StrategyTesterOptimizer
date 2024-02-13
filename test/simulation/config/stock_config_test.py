import unittest
import logging
from src.simulation.config import CandleConfig, TimeFrame


class StockConfig_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_equals_and_hash_THEN_correct(self):
    # Array
    base_s = CandleConfig("S1", TimeFrame.W)

    eq_stocks = [
        CandleConfig("S1", TimeFrame.W),
        CandleConfig("S1", TimeFrame.WEEK),
    ]

    not_eq_stocks = [
        CandleConfig("S2", TimeFrame.W),
        CandleConfig("S1", TimeFrame.H),
    ]
    # Act

    # Assert
    for asserted_sc in eq_stocks:
      self.assertEqual(hash(base_s), hash(asserted_sc), msg=asserted_sc)
      self.assertEqual(base_s, asserted_sc, msg=asserted_sc)

    for asserted_sc in not_eq_stocks:
      self.assertNotEqual(hash(base_s), hash(asserted_sc), msg=asserted_sc)
      self.assertNotEqual(base_s, asserted_sc, msg=asserted_sc)