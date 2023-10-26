import unittest
import logging
from src.strategy.run_config.market_config_sets import MarketConfigSets, date


class MarketConfigSets_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_add_set_THEN_it_immutable(self):
    # Array
    mcs = MarketConfigSets.Builder()\
        .add_stocks(["S1", "S2"], date(2020, 1, 1), date(2021, 1, 1))\
        .add_stocks(["S3", "S4"], date(2022, 1, 1), date(2023, 1, 1))\
        .build()

    # Act
    asserted_list = mcs.as_records()

    # Assert
    self.assertEqual(2, len(asserted_list))

    self.assertEqual(("S1", "S2"), asserted_list[0][0])
    self.assertEqual(date(2020, 1, 1), asserted_list[0][1])
    self.assertEqual(date(2021, 1, 1), asserted_list[0][2])

    self.assertEqual(("S3", "S4"), asserted_list[1][0])
    self.assertEqual(date(2022, 1, 1), asserted_list[1][1])
    self.assertEqual(date(2023, 1, 1), asserted_list[1][2])
