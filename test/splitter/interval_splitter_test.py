import unittest
import logging
from src.common.date_period import DatePeriod,date
from src.splitter.interval_splitter import split_period

class IntervalSplitter_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    

    def test_WHEN_split_array_THEN_split_correct_by_proportions(self):
        # Array

        # Act

        # Assert
        raise NotImplementedError('Test not implemented')

    def test_WHEN_split_array_of_datetime_THEN_split_correct_by_proportions_in_days(self):
        # Array
        
        # Act

        # Assert
        raise NotImplementedError('Test not implemented')
