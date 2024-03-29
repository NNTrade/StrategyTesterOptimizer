import unittest
import logging

from src.common.date_period import DatePeriod,date

class DatePeriod_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_request_period_in_years_THEN_get_correct_unsver(self):
    # Array
    dp = DatePeriod(date(2020, 1, 1), date(2021, 1, 1))
    # Act

    # Assert
    self.assertEqual(366, dp.period_in_days)
    self.assertAlmostEqual(366/365, dp.period_in_years,5)

  def test_WHEN_serialize_and_desetrialize_by_json_THEN_equal(self):
    # Array
    expected_cfg = DatePeriod(date(2020, 2, 3), date(2021, 5, 6))

    # Act
    json_str = expected_cfg.to_json()

    # Parse the JSON back into a DTO
    asserted_cfg = DatePeriod.from_json(json_str)
    
    # Assert
    self.assertEqual(expected_cfg, asserted_cfg)