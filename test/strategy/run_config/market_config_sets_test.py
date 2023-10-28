import unittest
import logging
from src.strategy.run_config.market_config_sets import MarketConfigSet, date


class MarketConfigSets_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_add_data_to_builder_THEN_build_correct_set(self):
    # Array
    mcs = MarketConfigSet.Builder()\
        .add_stocks(["S1", "S2"], date(2020, 1, 1), date(2021, 1, 1))\
        .add_stock("S3", date(2022, 1, 1), date(2023, 1, 1))\
        .build()

    # Act
    asserted_list = mcs.as_records()

    # Assert
    self.assertEqual(2, len(asserted_list))

    self.assertEqual(["S1", "S2"], asserted_list[0].stocks)
    self.assertEqual(date(2020, 1, 1), asserted_list[0].from_date)
    self.assertEqual(date(2021, 1, 1), asserted_list[0].untill_date)

    self.assertEqual(["S3"], asserted_list[1].stocks)
    self.assertEqual(date(2022, 1, 1), asserted_list[1].from_date)
    self.assertEqual(date(2023, 1, 1), asserted_list[1].untill_date)
