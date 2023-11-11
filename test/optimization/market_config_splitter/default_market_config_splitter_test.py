import unittest
import logging
from src.strategy.run_config import MarketConfig, date, StockConfig, TimeFrame, timedelta
from src.optimization.market_config_splitter import *

class MarketConfig_Split_On_Optiomization_Chunks_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                                                datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_give_wrong_intervals_THEN_get_errors(self):
        # Array
        #         
        # Act

        # Assert
        with self.assertRaises(AttributeError) as context:
            DefaultMarketConfigSplitter(timedelta(1),timedelta(1))
                                    
        with self.assertRaises(AttributeError) as context:
            DefaultMarketConfigSplitter(timedelta(3,hours=23),timedelta(1))
        
        with self.assertRaises(AttributeError) as context:
            DefaultMarketConfigSplitter(timedelta(8,1),timedelta(1))

        with self.assertRaises(AttributeError) as context:
            DefaultMarketConfigSplitter(timedelta(10),timedelta(1))

    def test_WHEN_forced_split_THEN_no_check_interval_relations(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 12))
        
        # Act

        # Assert
        DefaultMarketConfigSplitter(timedelta(1),timedelta(1), True)
                                    
        DefaultMarketConfigSplitter(timedelta(3,hours=23),timedelta(1), True,True)
        
        DefaultMarketConfigSplitter(timedelta(8,1),timedelta(1), True)

        DefaultMarketConfigSplitter(timedelta(10),timedelta(1), True)


    def test_WHEN_split_THEN_split_correct(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 10))
        expected_intervals = [
            ((date(2020, 1, 1), date(2020, 1, 5)),(date(2020, 1, 5), date(2020, 1, 6)) ),
            ((date(2020, 1, 2), date(2020, 1, 6)),(date(2020, 1, 6), date(2020, 1, 7)) ),
            ((date(2020, 1, 3), date(2020, 1, 7)),(date(2020, 1, 7), date(2020, 1, 8)) ),
            ((date(2020, 1, 4), date(2020, 1, 8)),(date(2020, 1, 8), date(2020, 1, 9)) ),
            ((date(2020, 1, 5), date(2020, 1, 9)),(date(2020, 1, 9), date(2020, 1, 10)) ),
        ]
        # Act
        asserted_tuples = DefaultMarketConfigSplitter(timedelta(4),timedelta(1)).split(mc1)

        # Assert
        self.assertEqual(5, len(asserted_tuples))
        for idx,expected_interval in enumerate(expected_intervals):
            expected_mc1 = MarketConfig([s1], TimeFrame.D, expected_interval[0][0], expected_interval[0][1])
            expected_mc2 = MarketConfig([s1], TimeFrame.D, expected_interval[1][0], expected_interval[1][1])
            self.assertEqual(expected_mc1, asserted_tuples[idx].optimization_config)
            self.assertEqual(expected_mc2, asserted_tuples[idx].forward_config)

    def test_WHEN_split_with_tail_THEN_raise_error(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 14))
        expected_intervals = [
            ((date(2020, 1, 1), date(2020, 1, 9)),(date(2020, 1, 9), date(2020, 1, 11)) ),
            ((date(2020, 1, 3), date(2020, 1, 11)),(date(2020, 1, 11), date(2020, 1, 13)) ),
        ]
        # Act
        # Assert
        with self.assertRaises(AttributeError) as context:
            DefaultMarketConfigSplitter(timedelta(8),timedelta(2)).split(mc1)

    def test_WHEN_split_with_cut_tail_THEN_raise_error(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 14))
        expected_intervals = [
            ((date(2020, 1, 1), date(2020, 1, 9)),(date(2020, 1, 9), date(2020, 1, 11)) ),
            ((date(2020, 1, 3), date(2020, 1, 11)),(date(2020, 1, 11), date(2020, 1, 13)) ),
        ]
        # Act
        asserted_tuples = DefaultMarketConfigSplitter(timedelta(8),timedelta(2), cut_tail=True).split(mc1)

        # Assert
        self.assertEqual(2, len(asserted_tuples))
        for idx,expected_interval in enumerate(expected_intervals):
            expected_mc1 = MarketConfig([s1], TimeFrame.D, expected_interval[0][0], expected_interval[0][1])
            expected_mc2 = MarketConfig([s1], TimeFrame.D, expected_interval[1][0], expected_interval[1][1])
            self.assertEqual(expected_mc1, asserted_tuples[idx].optimization_config)
            self.assertEqual(expected_mc2, asserted_tuples[idx].forward_config)

    def test_WHEN_cannt_split_THEN_return_empty(self):
        # Array
        s1 = StockConfig("A", TimeFrame.D)
        mc1 = MarketConfig([s1], TimeFrame.D, date(2020, 1, 1),
                           date(2020, 1, 5))
        # Act
        asserted_tuples = DefaultMarketConfigSplitter(timedelta(8),timedelta(1), cut_tail=True).split(mc1)
        
        # Assert
        self.assertEqual(0, len(asserted_tuples))
            