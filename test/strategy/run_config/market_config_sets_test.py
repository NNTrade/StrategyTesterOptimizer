import unittest
import logging
from src.strategy.run_config.market_config_sets import MarketConfigSet, date, TimeFrame, StockConfig


class MarketConfigSets_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_add_data_to_builder_THEN_build_correct_set(self):
    # Array
    s1 = StockConfig("S1", TimeFrame.D)
    s2 = StockConfig("S2", TimeFrame.D)
    s3 = StockConfig("S3", TimeFrame.W)
    mcs = MarketConfigSet.Builder()\
        .add_stocks(["S1", "S2"], TimeFrame.H, date(2020, 1, 1), date(2021, 1, 1), TimeFrame.D)\
        .add_stock("S3", TimeFrame.W, date(2022, 1, 1), date(2023, 1, 1))\
        .build()

    # Act
    asserted_list = mcs.as_records()

    # Assert
    self.assertEqual(2, len(asserted_list))

    self.assertEqual([s1, s2], asserted_list[0].stocks)
    self.assertEqual(TimeFrame.H, asserted_list[0].step_timeframe)
    self.assertEqual(date(2020, 1, 1), asserted_list[0].from_date)
    self.assertEqual(date(2021, 1, 1), asserted_list[0].untill_date)

    self.assertEqual([s3], asserted_list[1].stocks)
    self.assertEqual(TimeFrame.W, asserted_list[1].step_timeframe)
    self.assertEqual(date(2022, 1, 1), asserted_list[1].from_date)
    self.assertEqual(date(2023, 1, 1), asserted_list[1].untill_date)

  def test_WHEN_split_sharp_THEN_correct_splitting(self):
      # Array
      s1 = StockConfig("A", TimeFrame.D)
      mcs = MarketConfigSet.Builder()\
          .add_stocks(["S1"], TimeFrame.H, date(2020, 1, 1), date(2020, 1, 11), TimeFrame.D)\
          .add_stocks(["S2", "S3"], TimeFrame.H, date(2020, 2, 1), date(2020, 2, 10), TimeFrame.D)\
          .build()

      expected_mcs = MarketConfigSet.Builder()\
          .add_stocks(["S1"], TimeFrame.H, date(2020, 1, 1), date(2020, 1, 3), TimeFrame.D)\
          .add_stocks(["S1"], TimeFrame.H, date(2020, 1, 3), date(2020, 1, 5), TimeFrame.D)\
          .add_stocks(["S1"], TimeFrame.H, date(2020, 1, 5), date(2020, 1, 7), TimeFrame.D)\
          .add_stocks(["S1"], TimeFrame.H, date(2020, 1, 7), date(2020, 1, 9), TimeFrame.D)\
          .add_stocks(["S1"], TimeFrame.H, date(2020, 1, 9), date(2020, 1, 11), TimeFrame.D)\
          .add_stocks(["S2", "S3"], TimeFrame.H, date(2020, 2, 1), date(2020, 2, 3), TimeFrame.D)\
          .add_stocks(["S2", "S3"], TimeFrame.H, date(2020, 2, 3), date(2020, 2, 5), TimeFrame.D)\
          .add_stocks(["S2", "S3"], TimeFrame.H, date(2020, 2, 5), date(2020, 2, 7), TimeFrame.D)\
          .add_stocks(["S2", "S3"], TimeFrame.H, date(2020, 2, 7), date(2020, 2, 9), TimeFrame.D)\
          .add_stocks(["S2", "S3"], TimeFrame.H, date(2020, 2, 9), date(2020, 2, 11), TimeFrame.D)\
          .build()
      expected_records = expected_mcs.as_records()

      used_chuck_count = 5
      # Act

      asserted_mcs = mcs.split(used_chuck_count)
      asserted_records = asserted_mcs.as_records()
      # Assert
      self.assertEqual(used_chuck_count*2, len(asserted_records))
      for i in range(used_chuck_count):
          self.assertEqual(expected_records[i], asserted_records[i])

  # def test_WHEN_split_near_THEN_correct_splitting(self):
  #    # Array
  #    s1 = StockConfig("A", TimeFrame.D)
  #    mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
  #                        date(2020, 1, 11))
  #    expected_list = [
  #        MarketConfig([s1], TimeFrame.D, date(
  #            2020, 1, 1), date(2020, 1, 4)),
  #        MarketConfig([s1], TimeFrame.D, date(
  #            2020, 1, 4), date(2020, 1, 7)),
  #        MarketConfig([s1], TimeFrame.D, date(
  #            2020, 1, 7), date(2020, 1, 11))
  #    ]
  #    used_chuck_count = 3
  #    # Act
  #    asserted_list = mc1.split(used_chuck_count)
#
  #    # Assert
  #    self.assertEqual(used_chuck_count, len(asserted_list))
  #    for i in range(used_chuck_count):
  #        self.assertEqual(expected_list[i], asserted_list[i])
