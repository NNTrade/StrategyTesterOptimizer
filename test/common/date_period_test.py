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
    self.assertAlmostEquals(366/365, dp.period_in_years,5)
